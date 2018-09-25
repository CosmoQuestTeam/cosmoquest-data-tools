from cosmoquest_data_tools.annotation_library_transformer import AnnotationLibraryTransformer

import concurrent.futures
import random


class NoopAnnotationLibraryTransformer(AnnotationLibraryTransformer):
    """
    NOOP Annotation Library Transformer

    Useful for testing and as a skeleton
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def transform(self):
        results = list()

        with concurrent.futures.ProcessPoolExecutor(max_workers=self.workers) as executor:
            futures = list()

            for _ in range(100):
                futures.append(executor.submit(execute_transform))

            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                results.append(result)

        return self.annotation_library


# Instance Methods are not serializable by Pickle (when they have foreign data types, such as here) 
# Using a regular function is required for multiprocessing concurrency
def execute_transform():
    return None
