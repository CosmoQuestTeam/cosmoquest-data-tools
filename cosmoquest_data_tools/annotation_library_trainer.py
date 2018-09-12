import enum

from cosmoquest_data_tools.annotation_library import AnnotationLibrary


class AnnotationLibraryTrainerError(BaseException):
    pass


class AnnotationLibraryTrainers(enum.Enum):
    LUMINOTH = 0


class AnnotationLibraryTrainer:
    TRAINERS = {
        "LUMINOTH": AnnotationLibraryTrainers.LUMINOTH
    }

    algorithms = list()

    def __init__(self, **kwargs):
        self.annotation_library = kwargs["annotation_library"]

        self.model_path = kwargs.get("model_path")
        self.model = None

    def train(self, **kwargs):
        raise NotImplementedError

    def predict(self, image, **kwargs):
        raise NotImplementedError

    def predict_directory(self, directory, **kwargs):
        raise NotImplementedError

    @classmethod
    def execute(cls, annotation_library, trainer, trainer_kwargs=None):
        if not isinstance(annotation_library, AnnotationLibrary):
            raise AnnotationLibraryTrainerError("Provided 'annotation_library' should be an AnnotationLibrary object...")

        if trainer not in cls.TRAINERS:
            raise AnnotationLibraryTrainerError(f"Unknown provided 'trainer': '{trainer}'")

        if not isinstance(trainer_kwargs, dict):
            raise AnnotationLibraryTrainerError("Provided 'trainer_kwargs' should be a dict...")

        trainer_kwargs["annotation_library"] = annotation_library

        trainer = cls.TRAINERS[trainer]
        trainer_class = cls._get_trainer_class(trainer)

        trainer = trainer_class(**trainer_kwargs)
        return trainer.train(**trainer_kwargs)

    @staticmethod
    def _get_trainer_class(trainer):
        if trainer == AnnotationLibraryTrainers.LUMINOTH:
            from cosmoquest_data_tools.annotation_library_trainers.luminoth_annotation_library_trainer import LuminothAnnotationLibraryTrainer
            return LuminothAnnotationLibraryTrainer

        return None
