

class AnnotationLibraryBuilder:

    def __init__(self, targets=None, **kwargs):
        self.targets = targets or list()
    
    def build(self, kwargs=None):
        raise NotImplementedError()

    def detect_targets(self):
        raise NotImplementedError()

    def add_targets(self, targets):
        [self.add_target(target) for target in targets]

    def add_target(self, target):
        if target not in self.targets and self.validate_target(target):
            self.targets.append(target)

    def clear_targets(self):
        self.targets = list()

    def validate_targets(self):
        raise NotImplementedError()

    def validate_target(self):
        raise NotImplementedError()
