from cosmoquest_data_tools.annotation_library_transformer import AnnotationLibraryTransformer, AnnotationLibraryTransformerError
from cosmoquest_data_tools.annotation_library import AnnotationLibrary

from cosmoquest_data_tools.helpers.algorithms import non_maximum_suppression

from sklearn.cluster import KMeans

import enum
import concurrent.futures

import numpy as np


class BoundingBoxDeduplicateMode(enum.Enum):
    ALL = 0
    USER = 1


class BoundingBoxFiltrationAnnotationLibraryTransformer(AnnotationLibraryTransformer):
    DEDUPLICATE_MODES = {
        "ALL": BoundingBoxDeduplicateMode.ALL,
        "USER": BoundingBoxDeduplicateMode.USER
    }

    def __init__(self, **kwargs):
        self.deduplicate = kwargs.get("deduplicate") or False
        self.deduplicate_mode = kwargs.get("deduplicate_mode") or "USER"

        if self.deduplicate_mode not in self.DEDUPLICATE_MODES:
            raise AnnotationLibraryTransformerError(f"'deduplicate_mode' is expected to be one of: {', '.join(self.DEDUPLICATE_MODES.keys())}")

        self.deduplicate_mode = self.DEDUPLICATE_MODES[self.deduplicate_mode]

        super().__init__(**kwargs)

    def transform(self):
        with concurrent.futures.ProcessPoolExecutor(max_workers=self.workers) as executor:
            futures = list()

            processed_keys = 0
            filtered_bounding_boxes = 0

            for key in self.annotation_library.entries:
                futures.append(
                    executor.submit(
                        execute_transform, 
                        self.annotation_library.name,
                        key,
                        self.deduplicate,
                        self.deduplicate_mode
                    )
                )

            for future in concurrent.futures.as_completed(futures):
                key, bounding_boxes, filtered_count = future.result()

                filtered_bounding_boxes += filtered_count
                self.annotation_library.replace_bounding_boxes(key, bounding_boxes)

                processed_keys += 1
                print(f"{filtered_bounding_boxes} total bounding boxes filtered.")

                # Flush the HDF5 changes to disk every 200 keys
                if not processed_keys % 200:
                    self.annotation_library.flush()

        # self.annotation_library.repack()  ... TODO: repack breaks images atm... why?

        return self.annotation_library


# Instance Methods are not serializable by Pickle (when they have foreign data types, such as here) 
# Using a regular function is required for multiprocessing concurrency
def execute_transform(annotation_library_name, key, deduplicate, deduplicate_mode):
    annotation_library = AnnotationLibrary.load(annotation_library_name, read_only=True)

    # Get the Bounding Boxes
    bounding_boxes = annotation_library.get_bounding_boxes(key)

    # Index the Bounding Boxes
    bounding_box_index = dict()

    for bounding_box in bounding_boxes:
        index = f"{bounding_box['y0']}-{bounding_box['x0']}-{bounding_box['y1']}-{bounding_box['x1']}"
        bounding_box_index[index] = bounding_box

    filtered_bounding_boxes = list()

    # Deduplication
    if deduplicate:
        bounding_box_groups = dict()

        if deduplicate_mode == BoundingBoxDeduplicateMode.ALL:
            bounding_box_groups["ALL"] = bounding_boxes
        elif deduplicate_mode == BoundingBoxDeduplicateMode.USER:
            for bounding_box in bounding_boxes:
                if bounding_box["meta"] not in bounding_box_groups:
                    bounding_box_groups[bounding_box["meta"]] = list()

                bounding_box_groups[bounding_box["meta"]].append(bounding_box)

        for _, boxes in bounding_box_groups.items():
            if len(boxes) <= 5:
                filtered_bounding_boxes += boxes
                continue

            input_boxes = list()

            for box in boxes:
                input_boxes.append([box["y0"], box["x0"], box["y1"], box["x1"]])

            input_boxes = np.array(input_boxes)

            # Doing it twice cleans up boxes that are too close to boundaries of clusters
            output_boxes = cluster_bounding_boxes(input_boxes)
            output_boxes = cluster_bounding_boxes(output_boxes)

            for output_box in output_boxes:
                index = f"{output_box[0]}-{output_box[1]}-{output_box[2]}-{output_box[3]}"
                filtered_bounding_boxes.append(bounding_box_index[index])

    return key, filtered_bounding_boxes, (len(bounding_boxes) - len(filtered_bounding_boxes))


def cluster_bounding_boxes(bounding_boxes, clusters=2):
    input_areas = np.array(list(map(lambda bb: (bb[2] - bb[0]) * (bb[3] - bb[1]), bounding_boxes))).reshape(-1, 1)

    estimator = KMeans(init="k-means++", n_clusters=clusters, n_init=100)
    estimator.fit(input_areas)

    bounding_box_groups = [list() for _ in range(clusters)]

    for i, bounding_box in enumerate(bounding_boxes):
        bounding_box_groups[estimator.labels_[i]].append(bounding_box)

    output_bounding_boxes = list()    

    for bounding_box_group in bounding_box_groups:
        output_bounding_boxes += list(non_maximum_suppression(np.array(bounding_box_group), 0.1))

    return np.array(output_bounding_boxes)
