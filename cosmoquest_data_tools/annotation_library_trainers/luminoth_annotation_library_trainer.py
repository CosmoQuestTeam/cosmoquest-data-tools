from comet_ml import Experiment

from luminoth.tools.dataset.readers.object_detection import ObjectDetectionReader
from luminoth.tools.dataset.writers.object_detection_writer import ObjectDetectionWriter

from luminoth.utils.config import get_config

from cosmoquest_data_tools.annotation_library_trainer import AnnotationLibraryTrainer, AnnotationLibraryTrainerError
from cosmoquest_data_tools.helpers.luminoth import luminoth_train

from cosmoquest_data_tools.config import config

import os
import yaml

from datetime import datetime


class LuminothAnnotationLibraryTrainer(AnnotationLibraryTrainer):
    algorithms = ["fasterrcnn", "ssd"]

    def __init__(self, **kwargs):
        self.algorithm = kwargs.get("algorithm") or "fasterrcnn"

        if self.algorithm not in self.algorithms:
            raise AnnotationLibraryTrainerError(f"'algorithm' is expected to be one of: {', '.join(self.algorithms)}")

        super().__init__(**kwargs)

    def train(self, **kwargs):
        self._convert_annotation_library_to_tfrecords()

        luminoth_config, hyperparams = self._generate_train_config(**kwargs)

        experiment = Experiment(
            api_key=config["credentials"]["comet_ml"]["api_key"],
            project_name=config["credentials"]["comet_ml"]["project_name"],
            log_code=False,
            log_graph=False,
            auto_param_logging=False,
            auto_metric_logging=False,
            auto_output_logging=None,
            log_env_details=False,
            log_git_metadata=False
        )

        experiment.log_multiple_params(hyperparams)

        luminoth_train(luminoth_config, environment="local", experiment=experiment)

    def predict(self, image, **kwargs):
        pass

    def predict_directory(self, directory, **kwargs):
        pass

    def _convert_annotation_library_to_tfrecords(self):
        reader = LuminothAnnotationLibraryReader(self.annotation_library)

        writer = ObjectDetectionWriter(
            reader,
            "data",
            self.annotation_library.name
        )

        writer.save()

    def _generate_train_config(self, **kwargs):
        if self.algorithm == "fasterrcnn":
            train_config, hyperparams = self._generate_train_fasterrcnn_config(**kwargs)
        elif self.algorithm == "ssd":
            train_config, hyperparams = self._generate_train_ssd_config(**kwargs)

        if not os.path.exists("data/luminoth"):
            os.mkdir("data/luminoth")

        with open("data/luminoth/luminoth.yml", "w") as f:
            f.write(yaml.dump(train_config))

        return get_config("data/luminoth/luminoth.yml"), hyperparams

    def _generate_train_fasterrcnn_config(self, **kwargs):
        default_optimizer = {
            "_replace": True,
            "type": "momentum",
            "momentum": 0.9
        }

        train_config = {
            "train": {
                "seed": kwargs.get("seed"),
                "job_dir": "data/luminoth",
                "run_name": f"{self.annotation_library.name}_{datetime.now().strftime('%Y%m%d%H%M')}",
                "save_summaries_steps": None,
                "save_summaries_secs": None,
                "clip_by_norm": kwargs.get("clip_gradients") or False,
                "learning_rate": {
                    "_replace": True,
                    "decay_method": kwargs.get("learning_rate_decay"),
                    "learning_rate": kwargs.get("learning_rate") or 0.0003
                },
                "optimizer": kwargs.get("optimizer") or default_optimizer,
                "num_epochs": kwargs.get("epochs") or 1000
            },
            "dataset": {
                "type": "object_detection",
                "dir": "data",
                "split": self.annotation_library.name,
                "image_preprocessing": {
                    "min_size": 100,
                    "max_size": 1024
                },
                "data_augmentation": []
            },
            "model": {
                "type": "fasterrcnn",
                "network": {
                    "num_classes": len(self.annotation_library.annotation_classes)
                },
                "batch_norm": kwargs.get("use_batch_normalization") or False,
                "base_network": {
                    "architecture": kwargs.get("architecture") or "resnet_v1_101"
                },
                "anchors": {
                    "base_size": kwargs.get("anchor_size") or 256,
                    "scales": kwargs.get("anchor_scales") or [0.25, 0.5, 1, 2],
                    "ratios": kwargs.get("anchor_ratios") or [0.5, 1, 2],
                    "stride": kwargs.get("anchor_stride") or 16
                },
                "rcnn": {
                    "proposals": {
                        "class_max_detections": kwargs.get("max_proposals_per_class") or 100,
                        "class_nms_threshold": kwargs.get("non_maximum_suppression_threshold") or 0.5,
                        "total_max_detections": kwargs.get("max_proposals") or 300,
                        "min_prob_threshold": kwargs.get("minimum_probability") or 0.5
                    }
                }
            }
        }

        hyperparams = {
            "seed": train_config["train"]["seed"],
            "run_name": train_config["train"]["run_name"],
            "clip_gradients": train_config["train"]["clip_by_norm"],
            "learning_rate": train_config["train"]["learning_rate"]["learning_rate"],
            "optimizer": train_config["train"]["optimizer"]["type"],
            "epochs": train_config["train"]["num_epochs"],
            "algorithm": train_config["model"]["type"],
            "batch_normalization": train_config["model"]["batch_norm"],
            "architecture": train_config["model"]["base_network"]["architecture"],
            "anchor_size": train_config["model"]["anchors"]["base_size"],
            "anchor_scales": train_config["model"]["anchors"]["scales"],
            "anchor_ratios": train_config["model"]["anchors"]["ratios"],
            "anchor_stride": train_config["model"]["anchors"]["stride"],
            "max_proposals_per_class": train_config["model"]["rcnn"]["proposals"]["class_max_detections"],
            "non_maximum_suppression_threshold": train_config["model"]["rcnn"]["proposals"]["class_nms_threshold"],
            "max_proposals": train_config["model"]["rcnn"]["proposals"]["total_max_detections"],
            "minimum_probability": train_config["model"]["rcnn"]["proposals"]["min_prob_threshold"]cli
        }

        return train_config, hyperparams

    def _generate_train_ssd_config(self, **kwargs):
        # TODO: Implement SSD config. Not urgent. We are interested in Faster RCNN.
        return {}, {}


class LuminothAnnotationLibraryReader(ObjectDetectionReader):
    def __init__(self, annotation_library, **kwargs):
        super().__init__(**kwargs)

        self.annotation_library = annotation_library
        self.provided_classes = list(self.annotation_library.annotation_classes)

        self.yielded_records = 0
        self.errors = 0

    def get_total(self):
        return len(self.annotation_library.entries)

    def get_classes(self):
        return self.provided_classes

    def iterate(self):
        for key in self.annotation_library.entries:
            if self._stop_iteration():
                return
            try:
                image = self.annotation_library.get_image_bytes(key)
                image_shape = self.annotation_library.get_image_shape(key)
                bounding_boxes = self.annotation_library.get_bounding_boxes(key)
            except Exception as e:
                print(f"An exception got raised for key '{key}'")
                print(e, end="\n\n")
                continue

            formatted_bounding_boxes = list()

            for bounding_box in bounding_boxes:
                formatted_bounding_boxes.append({
                    "label": self.provided_classes.index(bounding_box["label"]),
                    "xmin": bounding_box["x0"],
                    "ymin": bounding_box["y0"],
                    "xmax": bounding_box["x1"],
                    "ymax": bounding_box["y1"]
                })

            if not len(formatted_bounding_boxes):
                continue

            self.yielded_records += 1

            yield {
                "width": image_shape[1],
                "height": image_shape[0],
                "depth": image_shape[2],
                "filename": key,
                "image_raw": image,
                "gt_boxes": formatted_bounding_boxes,
            }
