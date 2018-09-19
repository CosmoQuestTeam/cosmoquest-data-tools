import h5py
import os
import io
import subprocess
import shlex

import numpy as np

from PIL import Image

import skimage.color
import skimage.util

from hurry.filesize import size, alternative


class AnnotationLibrary:

    def __init__(self, name, file_path=None, read_only=False):
        self.name = name
        self.h5_file = h5py.File(file_path or self.file_path, "r" if read_only else "a")

        self.read_only = read_only

        self.keys = self._populate_keys()
        self.annotation_classes = self._populate_annotation_classes()

    @property
    def file_path(self):
        return f"data/{self.name}.alh5"

    @property
    def entries(self):
        return [key.decode("utf-8") for key in self.h5_file["keys"].value]

    def as_json_minimal(self):
        return {
            "name": self.name,
            "file_path": self.file_path,
            "file_size": size(os.path.getsize(self.file_path), system=alternative),
            "entry_count": len(self.entries),
            "annotation_classes": list(self.annotation_classes)
        }

    def as_json(self):
        pass

    def add_entry(self, key, field, data):
        self.keys.add(key.encode("utf-8"))
        self.h5_file.create_dataset(f"{key}-{field}", data=data)

    def add_complete_entry(self, entry):
        key = entry["file_location"].replace(".png", "")
        self.keys.add(key.encode("utf-8"))

        # Image Data
        with open(entry["file_location"], "rb") as f:
            image_bytes = f.read()

        self.h5_file.create_dataset(f"{key}-image", data=[image_bytes])

        image_bytes = None

        # Image Shape
        image_shape = (entry["height"], entry["width"], 3)
        self.h5_file.create_dataset(f"{key}-shape", data=image_shape)

        # Bounding Boxes
        bounding_boxes = list()

        for bounding_box in entry["bounding_boxes"]:
            annotation_class = bounding_box["annotation_class"].encode("utf-8")

            if "meta" not in bounding_box:
                bounding_box["meta"] = "N/A"

            meta = bounding_box["meta"].encode("utf-8")

            bounding_boxes.append((
                bounding_box["top"],
                bounding_box["left"],
                bounding_box["bottom"],
                bounding_box["right"],
                annotation_class,
                meta
            ))

            self.annotation_classes.add(annotation_class)

        self.h5_file.create_dataset(f"{key}-bounding-boxes", data=bounding_boxes)

    def get_entry(self, key, field):
        return self.h5_file[f"{key}-{field}"].value

    def get_image_bytes(self, key):
        return self.get_entry(key, "image")[0]

    def get_image_array(self, key):
        image_array = np.array(Image.open(io.BytesIO(self.get_image_bytes(key))), dtype="uint8")

        # The image sets are mixes of 2 and 3 channel images
        # We are going to make sure we only work with 3, for consistency        
        if len(image_array.shape) == 2:
            image_array = skimage.util.img_as_ubyte(skimage.color.gray2rgb(image_array))

        return image_array

    def get_image_shape(self, key):
        return [int(i) for i in self.get_entry(key, "shape")]

    def get_bounding_boxes(self, key):
        return self._format_bounding_boxes(self.get_entry(key, "bounding-boxes"))

    def replace_bounding_boxes(self, key, bounding_boxes):
        bounding_boxes = self._encode_bounding_boxes(bounding_boxes)
        key = f"{key}-bounding-boxes"

        del self.h5_file[key]
        self.h5_file.create_dataset(key, data=bounding_boxes)

    def flush(self):
        self.h5_file.flush()

    def commit(self):
        self.commit_keys()
        self.commit_annotation_classes()

    def commit_keys(self):
        if "keys" in self.h5_file:
            del self.h5_file["keys"]

        self.h5_file.create_dataset("keys", data=list(self.keys))

    def commit_annotation_classes(self):
        if "annotation_classes" in self.h5_file:
            del self.h5_file["annotation_classes"]

        self.h5_file.create_dataset("annotation_classes", data=list(self.annotation_classes))

    # In HDF5, due to the sequential nature of the writing, the space occupied by altered / deleted items is not reclaimed
    # Repacking is one way around this downside.
    def repack(self):
        self.h5_file.close()

        FNULL = open(os.devnull, "w")
        subprocess.call(shlex.split(f"ptrepack {self.file_path} {self.file_path}.tmp"), stdout=FNULL, stderr=subprocess.STDOUT)
        FNULL.close()

        os.remove(self.file_path)
        os.rename(f"{self.file_path}.tmp", self.file_path)

        self.h5_file = h5py.File(self.file_path, "r" if self.read_only else "a")

    def _populate_keys(self):
        if "keys" in self.h5_file:
            return set([key.decode("utf-8") for key in self.h5_file["keys"].value])
        else:
            return set()

    def _populate_annotation_classes(self):
        if "annotation_classes" in self.h5_file:
            return set([annotation_class.decode("utf-8") for annotation_class in self.h5_file["annotation_classes"].value])
        else:
            return set()

    # Go from encoded in HDF5 dataset to dict
    def _format_bounding_boxes(self, bounding_boxes):
        return [self._format_bounding_box(bounding_box) for bounding_box in bounding_boxes]

    def _format_bounding_box(self, bounding_box):
        return {
            "y0": int(float(bounding_box[0])),
            "x0": int(float(bounding_box[1])),
            "y1": int(float(bounding_box[2])),
            "x1": int(float(bounding_box[3])),
            "label": bounding_box[4].decode("utf-8"),
            "meta": bounding_box[5].decode("utf-8")
        }

    # Go from dict to encoded in HDF5 dataset
    def _encode_bounding_boxes(self, bounding_boxes):
        return [self._encode_bounding_box(bounding_box) for bounding_box in bounding_boxes]

    def _encode_bounding_box(self, bounding_box):
        return [
            bounding_box["y0"],
            bounding_box["x0"],
            bounding_box["y1"],
            bounding_box["x1"],
            bounding_box["label"].encode("utf-8"),
            (bounding_box["meta"] or "N/A").encode("utf-8")
        ]

    @classmethod
    def load(cls, name_or_path, **kwargs):
        if os.path.isfile(name_or_path):
            file_path = name_or_path
            name = name_or_path.split("/")[-1].replace(".alh5", "")
        else:
            name = name_or_path
            file_path = f"data/{name_or_path}.alh5"

            if not os.path.isfile(file_path):
                raise FileNotFoundError(file_path)

        return cls(name, file_path=file_path, **kwargs)

    @classmethod
    def discover(cls, path):
        if not os.path.isdir(path):
            raise FileNotFoundError(path)

        annotation_library_file_paths = list()

        for root, dirs, files in os.walk(path):
            if root != path:
                break

            for file in files:
                if file.endswith(".alh5"):
                    annotation_library_file_paths.append(f"{root}/{file}")

        return [cls.load(file_path, read_only=True) for file_path in annotation_library_file_paths]
