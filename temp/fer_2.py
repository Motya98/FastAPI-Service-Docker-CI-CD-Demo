import json
import pickle
import pandas as pd
import os
from sklearn.preprocessing import StandardScaler, Normalizer
from sklearn.preprocessing import PolynomialFeatures



for m in os.listdir('models'):
    with open(f"models\\{m}", 'rb') as f:
        model = pickle.load(f)

        with open('PSEVEN_INFO.json', 'r') as file:
            pseven_info = json.load(file)
        df = pd.read_csv(pseven_info['data_path'])
        x = df[df.columns[0:4]]

        degree = int(m.split('Degree')[1].split('_')[0])
        if degree != 1:
            polynominal_converter = PolynomialFeatures(degree)
            polynominal_converter.fit(x)
            x = polynominal_converter.transform(x)

        scaler = Normalizer()
        scaler.fit(x)
        x = scaler.transform(x)


        y_pred = model.predict(x)





""" Для полинома первой степени
for m in os.listdir('models'):
    with open(f"models\\{m}", 'rb') as f:
        model = pickle.load(f)

        df = pd.read_csv(r'C:\\Users\\barha\\PycharmProjects\\Machine Learning\\ML\\Boston.csv')
        x = df[df.columns[0:12]]

        scaler = Normalizer()
        scaler.fit(x)
        x = scaler.transform(x)


        y_pred = model.predict(x)
"""