import enum

from cosmoquest_data_tools.annotation_library import AnnotationLibrary


class AnnotationLibraryTransformerError(BaseException):
    pass


class AnnotationLibraryTransformers(enum.Enum):
    NOOP = 0
    IMAGE_AUGMENTATION = 1
    BOUNDING_BOX_FILTRATION = 2


class AnnotationLibraryTransformer:

    TRANSFORMERS = {
        "NOOP": AnnotationLibraryTransformers.NOOP,
        "IMAGE_AUGMENTATION": AnnotationLibraryTransformers.IMAGE_AUGMENTATION,
        "BOUNDING_BOX_FILTRATION": AnnotationLibraryTransformers.BOUNDING_BOX_FILTRATION
    }

    def __init__(self, **kwargs):
        # Execution of transformations is concurrent for major speedups
        self.workers = kwargs.get("workers")  # A value of 'None' here will default to the number of CPUs

        self.annotation_library = kwargs["annotation_library"]  # expected

    def transform(self):
        raise NotImplementedError

    @classmethod
    def execute(cls, annotation_library, transformer, transformer_kwargs=None):
        if not isinstance(annotation_library, AnnotationLibrary):
            raise AnnotationLibraryTransformerError("Provided 'annotation_library' should be an AnnotationLibrary object...")

        if transformer not in cls.TRANSFORMERS:
            raise AnnotationLibraryTransformerError(f"Unknown provided 'transformer': '{transformer}'")

        if not isinstance(transformer_kwargs, dict):
            raise AnnotationLibraryTransformerError("Provided 'transformer_kwargs' should be a dict...")

        transformer_kwargs["annotation_library"] = annotation_library

        transformer = cls.TRANSFORMERS[transformer]
        transformer_class = cls._get_transformer_class(transformer)

        transformer = transformer_class(**transformer_kwargs)
        return transformer.transform()
        
    @staticmethod
    def _get_transformer_class(transformer):
        if transformer == AnnotationLibraryTransformers.NOOP:
            from cosmoquest_data_tools.annotation_library_transformers.noop_annotation_library_transformer import NoopAnnotationLibraryTransformer
            return NoopAnnotationLibraryTransformer
        elif transformer == AnnotationLibraryTransformers.IMAGE_AUGMENTATION:
            from cosmoquest_data_tools.annotation_library_transformers.image_augmentation_annotation_library_transformer import ImageAugmentationAnnotationLibraryTransformer
            return ImageAugmentationAnnotationLibraryTransformer
        elif transformer == AnnotationLibraryTransformers.BOUNDING_BOX_FILTRATION:
            from cosmoquest_data_tools.annotation_library_transformers.bounding_box_filtration_annotation_library_transformer import BoundingBoxFiltrationAnnotationLibraryTransformer
            return BoundingBoxFiltrationAnnotationLibraryTransformer

        return None
