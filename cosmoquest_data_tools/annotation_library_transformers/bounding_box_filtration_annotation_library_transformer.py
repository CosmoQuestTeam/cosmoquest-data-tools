from cosmoquest_data_tools.annotation_library_transformer import AnnotationLibraryTransformer


class BoundingBoxFiltrationAnnotationLibraryTransformer(AnnotationLibraryTransformer):

    def __init__(self, **kwargs):
        print("HI")

        super().__init__(**kwargs)
