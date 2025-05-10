import abc


class StructurePredict(abc.ABC):
    @abc.abstractmethod
    def prepare_framework_models(self):
        pass

    @abc.abstractmethod
    def manage_processes_create_model(self):
        pass

    @abc.abstractmethod
    def create_model(self):
        pass

    @abc.abstractmethod
    def search_best_model(self):
        pass

    @abc.abstractmethod
    def predict_model(self):
        pass

    @abc.abstractmethod
    def error_model(self):
        pass
