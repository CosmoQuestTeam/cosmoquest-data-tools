import os
import requests

from concurrent.futures import ThreadPoolExecutor

from pony.orm import db_session

from cosmoquest_data_tools.annotation_library_builder import AnnotationLibraryBuilder
from cosmoquest_data_tools.annotation_library import AnnotationLibrary


class CosmoquestAnnotationLibraryBuilder(AnnotationLibraryBuilder):
    """
    Build Annotation Libraries from data found in the Cosmoquest databases.

    Valid Targets: Cosmoquest users

    The database should be one of: 'live', 'sandbox'
    """

    def __init__(
        self,
        application=None,
        database="live",
        annotation_class="crater",
        image_shape=(450, 450)
    ):
        self.application = application
        self.annotation_class = annotation_class
        self.image_shape = image_shape
        
        if database not in ["live", "sandbox"]:
            database = "live"

        self.database = database

        # Import the correct models, based on provided database kwarg
        if self.database == "live":
            from cosmoquest_data_tools.models.cosmoquest_legacy import User, Image, Mark
        elif self.database == "sandbox":
            pass  # from cosmoquest_data_tools.models.cosmoquest_django import User, Image, Mark

        self.models = {
            "User": User,
            "Image": Image,
            "Mark": Mark
        }

        self.existing_images = set()
        self.bounding_boxes = dict()

        # Build a mapping of Image IDs => Image file locations
        self.image_urls = self._cache_image_file_locations()

        targets = None

        super().__init__(targets=targets)

    @db_session
    def build(self, name):
        if not len(self.targets):
            return None
        
        annotation_library = AnnotationLibrary(name)

        for target in self.targets:
            print(f"Collecting data for user '{target}'...")

            # Build a set of existing image files
            self.existing_images = self._scan_for_existing_images()

            # Fetch the target user
            user = self.models["User"].get(name=target)
            
            # Fetch the target user's marks within the scoped in application
            marks = self.models["Mark"].select(lambda m: m.application.name == self.application and m.user == user)[:]

            # Build a set of the unique encoutered images
            images = [self.image_urls[image_id] for image_id in set([m.image.id for m in marks])]

            print(f"Found {len(marks)} marks in {len(images)} images for user '{target}' in application '{self.application}'...", end="\n\n")

            # Synchronize images to disk, for those we don't have yet
            self._sync_images(images)

            # Generate and append the bounding boxes from marks
            self._generate_bounding_boxes(marks, target)

        for file_name, bounding_boxes in self.bounding_boxes.items():
            entry = {
                "file_location": f"data/images/{self.application}/{file_name}",
                "width": self.image_shape[1],
                "height": self.image_shape[0],
                "bounding_boxes": bounding_boxes
            }

            annotation_library.add_entry(entry)

        annotation_library.commit()

        return annotation_library

    def validate_targets(self, targets):
        print("Validating targets...", end="\n\n")
        return [target for target in targets if self.validate_target(target)]

    @db_session
    def validate_target(self, target):
        print(f"Validating target: {target}", end=" ")
        valid = True

        user = self.models["User"].get(name=target)

        if user is None:
            valid = False
        elif self.models["Mark"].select(lambda m: m.application.name == self.application and m.user == user).count() < 1:
            valid = False

        print(f"... {valid}")
        return valid

    @db_session
    def _cache_image_file_locations(self):
        image_file_locations = dict()

        print(f"Caching image file locations for '{self.application}' application...")

        images = self.models["Image"].select(lambda i: i.application.name == self.application)[:]

        print(f"Found {len(images)} image(s)...")

        for image in images:
            image_file_locations[image.id] = image.file_location

        print("Done!", end="\n\n")

        return image_file_locations

    def _scan_for_existing_images(self):
        existing_images = set()

        print(f"Scanning for existing images for '{self.application}' application...")

        if not os.path.isdir("data/images"):
            os.mkdir("data/images")

        image_directory = f"data/images/{self.application}"

        if not os.path.isdir(image_directory):
            os.mkdir(image_directory)
            return existing_images

        for root, _, files in os.walk(image_directory):
            if root == image_directory:
                for file in files:
                    if file.endswith(".png"):
                        existing_images.add(file)
            else:
                break

        print(f"Found {len(existing_images)} existing images!", end="\n\n")

        return existing_images

    def _sync_images(self, image_urls):
        with ThreadPoolExecutor() as executor:
            for image_url in image_urls:
                file_name = "_".join(image_url.split("/")[-3:])

                if file_name not in self.existing_images:
                    executor.submit(self._download_image, image_url, file_name)

    def _download_image(self, image_url, file_name):
        print(f"Downloading '{image_url}'...")

        with open(f"data/images/{self.application}/{file_name}", "wb") as f:
            response = requests.get(image_url)
            f.write(response.content)

    def _generate_bounding_boxes(self, marks, user):
        for mark in marks:
            # Some data is garbage in the DB; filter it
            if mark.diameter is None or mark.x is None or mark.y is None:
                continue

            image_url = self.image_urls[mark.image.id]
            file_name = "_".join(image_url.split("/")[-3:])

            if file_name not in self.bounding_boxes:
                self.bounding_boxes[file_name] = []

            radius = mark.diameter / 2.0

            y0 = mark.y - radius
            x0 = mark.x - radius
            y1 = mark.y + radius
            x1 = mark.x + radius

            self.bounding_boxes[file_name].append({
                "top": y0,
                "left": x0,
                "bottom": y1,
                "right": x1,
                "annotation_class": self.annotation_class,
                "meta": user
            })
