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
