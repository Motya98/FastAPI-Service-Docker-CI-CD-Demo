from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
import pandas as pd
import seaborn as sns
from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import StandardScaler, Normalizer
import json
import multiprocessing
import pickle
import time

class Predict:
    def __init__(self, x):
        self.x = x


    def polyniminal_model(self):
        if self.poly_bool != 1:
            polynominal_converter = PolynomialFeatures(degree=self.poly_bool)
            polynominal_converter.fit(self.x)
            self.x = polynominal_converter.transform(self.x)


    def standartization_data(self):
        scaler = Normalizer()
        scaler.fit(self.x)
        self.x = scaler.transform(self.x)


    def predict(self):
        with open(f"models\\{self.method}", 'rb') as f:
            model = pickle.load(f)
        self.y = model.predict(self.x)
        self.df = pd.DataFrame(self.y, columns=[self.name_y])
        self.memory.put(self.df)


    def go(self, name_y, poly_bool, memory, method):
        self.name_y = name_y
        self.poly_bool = poly_bool
        self.memory = memory
        self.method = method
        self.polyniminal_model()
        self.standartization_data()
        self.predict()



if __name__ == '__main__':
    with open('PSEVEN_INFO.json', 'r') as file:
        pseven_info = json.load(file)
    x = pd.read_csv(pseven_info['data_for_predict'])[pd.read_csv(pseven_info['data_for_predict']).columns[0:pseven_info['x']]]

    with open('best_sorted_models_info.json', 'r') as file:
        best_sorted_models_info = json.load(file)

    list_name_y = [value['name_y'] for value in best_sorted_models_info.values()]
    list_degree = [value['degree'] for value in best_sorted_models_info.values()]
    list_memory = [multiprocessing.Queue() for i in range(len(best_sorted_models_info.keys()))]
    list_method = [key for key in best_sorted_models_info.keys()]
    list_processes = [multiprocessing.Process(target=Predict(x).go, args=(list_name_y[i], list_degree[i], list_memory[i],
                                                                          list_method[i])) for i in range(len(best_sorted_models_info.keys()))]
    [i.start() for i in list_processes]
    [i.join() for i in list_processes]
    temp_df_all_y = pd.concat([i.get() for i in list_memory], axis=1)
    temp_df_all = pd.concat([x, temp_df_all_y], axis=1)
    temp_df_all.to_csv('data_predictions.csv', index=False)
    with open('bool.txt', 'w') as file:
        file.write('End')

"""
1. получить файл со входными данными для степени полниномизации
2. открыть бест моделс 
3. сделать нормализацию и полиномилинизацию
3. для каждой модели из бест моделс выполнить прдсказание, сохранить датафрейм только с предсказанными значениями
"""