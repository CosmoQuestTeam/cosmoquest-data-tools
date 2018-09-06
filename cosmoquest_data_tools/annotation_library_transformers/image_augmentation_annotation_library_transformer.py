from cosmoquest_data_tools.annotation_library_transformer import AnnotationLibraryTransformer, AnnotationLibraryTransformerError
from cosmoquest_data_tools.annotation_library import AnnotationLibrary

from cosmoquest_data_tools.helpers.image_augmentation_pipelines import IMAGE_AUGMENTATION_PIPELINES

import io
import os
import shutil

import concurrent.futures

import imgaug as ia

from PIL import Image


class ImageAugmentationAnnotationLibraryTransformer(AnnotationLibraryTransformer):

    def __init__(self, **kwargs):
        self.image_augmentation_pipeline = kwargs.get("image_augmentation_pipeline") or "DEFAULT"

        if self.image_augmentation_pipeline not in IMAGE_AUGMENTATION_PIPELINES:
            raise AnnotationLibraryTransformerError(f"'image_augmentation_pipeline' is required and expected to be one of: {', '.join(IMAGE_AUGMENTATION_PIPELINES.keys())}")

        self.augmentation_count = kwargs.get("augmentation_count") or 4

        super().__init__(**kwargs)

    def transform(self):
        chunk_size = self.workers * 10
        offset = 0

        keys = self.annotation_library.entries[:]

        # Make a copy for the workers to read off of
        shutil.copyfile(self.annotation_library.file_path, f"{self.annotation_library.file_path}.tmp")

        while True:
            with concurrent.futures.ProcessPoolExecutor(max_workers=self.workers) as executor:
                chunk_start = offset
                chunk_end = offset + chunk_size

                print(f"Performing {self.augmentation_count} augmentations for images {chunk_start} to {chunk_end}...")

                if chunk_end >= len(keys):
                    chunk_end = -1

                futures = list()

                for key in keys[chunk_start:chunk_end]:
                    futures.append(
                        executor.submit(
                            execute_transform, 
                            f"{self.annotation_library.file_path}.tmp",
                            key,
                            self.image_augmentation_pipeline,
                            self.augmentation_count
                        )
                    )

                for future in concurrent.futures.as_completed(futures):
                    try:
                        result = future.result()
                    except Exception as e:
                        print(e)
                        continue               

                    for entry in result:
                        self.annotation_library.add_entry(entry[0], "image", [entry[1]])
                        self.annotation_library.add_entry(entry[0], "shape", entry[2])
                        self.annotation_library.add_entry(entry[0], "bounding-boxes", entry[3])

                    result = None

                self.annotation_library.flush()

                if chunk_end == -1:
                    break

                offset += chunk_size

        self.annotation_library.commit()

        os.remove(f"{self.annotation_library.file_path}.tmp")

        return self.annotation_library


# Instance Methods are not serializable by Pickle (when they have foreign data types, such as here) 
# Using a regular function is required for multiprocessing concurrency
def execute_transform(annotation_library_file_path, key, image_augmentation_pipeline, augmentation_count):
    annotation_library = AnnotationLibrary.load(annotation_library_file_path, read_only=True)
    image_augmentation_pipeline = IMAGE_AUGMENTATION_PIPELINES[image_augmentation_pipeline]()

    # Get the Image Data
    image_array = annotation_library.get_image_array(key)
    height, width, channels = image_array.shape

    # Get the Bounding Boxes
    bounding_boxes = annotation_library.get_bounding_boxes(key)

    # Prepare the Bounding Boxes for Image Augmentation
    ia_bounding_boxes = list()

    for bounding_box in bounding_boxes:
        y0 = float(bounding_box["y0"])
        x0 = float(bounding_box["x0"])
        y1 = float(bounding_box["y1"])
        x1 = float(bounding_box["x1"])

        is_valid = y0 >= 0 and x0 >= 0 and y1 < height and x1 < width

        if not is_valid:
            continue

        ia_bounding_boxes.append(ia.BoundingBox(x1=x0, y1=y0, x2=x1, y2=y1, label=f"{bounding_box['label']}###{bounding_box['meta']}"))

    ia_bounding_boxes =  ia.BoundingBoxesOnImage(ia_bounding_boxes, shape=image_array.shape)

    # Image Augmentation
    result = list()
    
    for i in range(augmentation_count):
        new_key = f"{key}_{i}"
        pipeline = image_augmentation_pipeline.to_deterministic()

        augmented_image = pipeline.augment_images([image_array])[0]
        augmented_bounding_boxes = pipeline.augment_bounding_boxes([ia_bounding_boxes])[0]

        # Format data for inter-process communication
        image = Image.fromarray(augmented_image)

        image_bytes = io.BytesIO()
        image.save(image_bytes, format="PNG")

        image_bytes.seek(0)
        image_bytes = image_bytes.read()

        formatted_bounding_boxes = list()

        for bounding_box in augmented_bounding_boxes.bounding_boxes:
            label, meta = bounding_box.label.split("###")

            formatted_bounding_boxes.append([
                bounding_box.y1,
                bounding_box.x1,
                bounding_box.y2,
                bounding_box.x2,
                label.encode("utf-8"),
                meta.encode("utf-8")
            ])

        result.append((new_key, image_bytes, (height, width, channels), formatted_bounding_boxes))

    return result
