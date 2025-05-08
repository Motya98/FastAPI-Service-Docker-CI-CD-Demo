import abc


class Structure(abc.ABC):
    @abc.abstractmethod
    def preprocess_data(self):
        pass

    @abc.abstractmethod
    def polynomial_model(self):
        pass

    @abc.abstractmethod
    def train_test_split_data(self):
        pass

    @abc.abstractmethod
    def standartization_data(self):
        pass

    @abc.abstractmethod
    def create_grid_model(self):
        pass

    @abc.abstractmethod
    def fit_model(self):
        pass

    @abc.abstractmethod
    def pred_model(self):
        pass

    @abc.abstractmethod
    def error_model(self):
        pass
