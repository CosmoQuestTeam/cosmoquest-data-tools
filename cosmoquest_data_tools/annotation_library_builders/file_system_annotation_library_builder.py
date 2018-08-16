import os
import json

from cosmoquest_data_tools.annotation_library_builder import AnnotationLibraryBuilder
from cosmoquest_data_tools.annotation_library import AnnotationLibrary


class FileSystemAnnotationLibraryBuilder(AnnotationLibraryBuilder):
    """
    Build Annotation Libraries from data found on the local file system.
    
    Ideally, Annotation Libraries should be built from a ComsoquestAnnotationLibraryBuilder
    but legacy datasets require the use of this builder.

    Valid Targets: 'sub_image_data.json' files in a provided directory tree

    The base directory should be a valid path to the relative file locations in the 'sub_image_data.json'
    """

    def __init__(
        self,
        base_directory=None,
        automatic_target_detection=True
    ):
        self.base_directory = base_directory

        targets = None

        if automatic_target_detection:
            if self.base_directory is not None and os.path.isdir(self.base_directory):
                targets = self.detect_targets()

        super().__init__(targets=targets)

    def build(self, name):
        if not len(self.targets):
            return None
        
        annotation_library = AnnotationLibrary(name)

        for target in self.targets:
            with open(target, "r") as f:
                entries = json.loads(f.read())

            for entry in entries:
                # Exception for craters legacy files...
                if "craters" in entry:
                    entry["bounding_boxes"] = entry["craters"]

                    for bounding_box in entry["bounding_boxes"]:
                        bounding_box["annotation_class"] = "crater"

                entry["file_location"] = f"{self.base_directory}/{entry['file_location']}"
                annotation_library.add_entry(entry)
        
        annotation_library.commit()

        return annotation_library

    def detect_targets(self):
        targets = list()

        for root, dirs, files in os.walk(self.base_directory):
            if "sub_image_data.json" in files:
                targets.append(f"{root}/sub_image_data.json".replace("\\", "/"))

        if len(targets):
            targets = self.validate_targets(targets)

        return targets

    def validate_targets(self, targets):
        print("Validating targets...", end="\n\n")
        return [target for target in targets if self.validate_target(target)]

    def validate_target(self, target):
        print(f"Validating target: {target}", end=" ")
        valid = True

        with open(target, "r") as f:
            data = json.loads(f.read())

            if not len(data):
                return False

            sample = data[0]

            if "file_location" not in sample:
                valid = False
            elif "width" not in sample:
                valid = False
            elif "height" not in sample:
                valid = False
            elif "bounding_boxes" not in sample and "craters" not in sample:
                valid = False

        print(f"... {valid}")
        return valid
