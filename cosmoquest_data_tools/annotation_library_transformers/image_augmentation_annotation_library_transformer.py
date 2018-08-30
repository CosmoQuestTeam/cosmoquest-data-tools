from cosmoquest_data_tools.annotation_library_transformer import AnnotationLibraryTransformer, AnnotationLibraryTransformerError
from cosmoquest_data_tools.annotation_library import AnnotationLibrary

from cosmoquest_data_tools.helpers.image_augmentation_pipelines import IMAGE_AUGMENTATION_PIPELINES

import concurrent.futures


class ImageAugmentationAnnotationLibraryTransformer(AnnotationLibraryTransformer):

    def __init__(self, **kwargs):
        self.image_augmentation_pipeline = kwargs.get("image_augmentation_pipeline") or "DEFAULT"

        if self.image_augmentation_pipeline not in IMAGE_AUGMENTATION_PIPELINES:
            raise AnnotationLibraryTransformerError(f"'image_augmentation_pipeline' is required and expected to be one of: {', '.join(IMAGE_AUGMENTATION_PIPELINES.keys())}")

        super().__init__(**kwargs)

    def transform(self):
        with concurrent.futures.ProcessPoolExecutor(max_workers=self.workers) as executor:
            futures = list()

            for key in self.annotation_library.entries[:10]:
                futures.append(
                    executor.submit(
                        execute_transform, 
                        self.annotation_library.name,
                        key,
                        self.image_augmentation_pipeline
                    )
                )

            for future in concurrent.futures.as_completed(futures):
                result = future.result()

        return self.annotation_library

# Instance Methods are not serializable by Pickle (when they have foreign data types, such as here) 
# Using a regular function is required for multiprocessing concurrency
def execute_transform(annotation_library_name, key, image_augmentation_pipeline):
    annotation_library = AnnotationLibrary.load(annotation_library_name, read_only=True)
    image_augmentation_pipeline = IMAGE_AUGMENTATION_PIPELINES[image_augmentation_pipeline]()

    # Get the Image Data
    image_array = annotation_library.get_image_array(key)
    height, width, channels = image_array.shape

    # Get the Bounding Boxes
    bounding_boxes = annotation_library.get_bounding_boxes(key)


    print(key)
