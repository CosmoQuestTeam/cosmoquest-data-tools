import datetime
import h5py


class AnnotationLibrary:

    def __init__(self, name, file_path=None):
        self.name = name
        self.h5_file = h5py.File(file_path or self.file_path, "a")

        self.keys = self._populate_keys()
        self.annotation_classes = self._populate_annotation_classes()
        
    @property
    def file_path(self):
        return f"data/{self.name}_{datetime.datetime.utcnow().strftime('%Y%m%d')}.alh5"

    def add_entry(self, entry):
        key = entry["file_location"].replace(".png", "")
        self.keys.append(key.encode("utf-8"))
        
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

    def commit(self):
        self.commit_keys()
        self.commit_annotation_classes()

    def commit_keys(self):
        if "keys" in self.h5_file:
            del self.h5_file["keys"]

        self.h5_file.create_dataset("keys", data=self.keys)

    def commit_annotation_classes(self):
        if "annotation_classes" in self.h5_file:
            del self.h5_file["annotation_classes"]

        self.h5_file.create_dataset("annotation_classes", data=list(self.annotation_classes))

    def _populate_keys(self):
        if "keys" in self.h5_file:
            return self.h5_file["keys"].value
        else:
            return list()

    def _populate_annotation_classes(self):
        if "annotation_classes" in self.h5_file:
            return set(self.h5_file["annotation_classes"].value)
        else:
            return set()

    @classmethod
    def load(cls, h5_path):
        pass