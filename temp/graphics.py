import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import json
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import StandardScaler, Normalizer
from PIL import Image, ImageDraw, ImageFont

def graphics():
    def pred(model, x_dataframe, degree):
        if degree != 1:
            polynominal_converter = PolynomialFeatures(degree=degree)
            polynominal_converter.fit(x_dataframe)
            x_dataframe = polynominal_converter.transform(x_dataframe)

        scaler = Normalizer()
        scaler.fit(x_dataframe)
        x_dataframe = scaler.transform(x_dataframe)

        y_pred = model.predict(x_dataframe)
        return y_pred


    with open('best_sorted_models_info.json', 'r') as file:
        best_sorted_models_info = json.load(file)
    with open('PSEVEN_INFO.json', 'r') as file:
        pseven_info = json.load(file)
        df = pd.DataFrame(pd.read_csv(pseven_info['data_path']))
    for key, value in best_sorted_models_info.items():
        with open(f"models\\{key}", 'rb') as f:
            model = pickle.load(f)
        sns.pairplot(data=df, corner=True)
        plt.savefig(f"graphics\\{value['name_y']}")
        plt.close()

        with open(f"models\\{key}", 'rb') as f:
            model = pickle.load(f)
            x_dataframe = df[df.columns[0:pseven_info['x']]]
            degree = best_sorted_models_info[key]['degree']
        y_pred = pred(model, x_dataframe, degree)

        for x_ in range(pseven_info['x']):
            data = pd.concat([df[df.columns[x_]], df[value['name_y']]], axis=1)
            sns.scatterplot(data=data, x=data[data.columns[0]], y=data[data.columns[1]], color='red')
            plt.plot(data[data.columns[0]], y_pred, color='#30d5c8', marker='*', markerfacecolor='black', alpha=0.1)
            plt.savefig(f"""graphics\\{str([i for i in data.columns]).replace("'", '').replace("[", "").replace("]", "")}""")
            plt.close()

    for key, value in best_sorted_models_info.items():
        degree = best_sorted_models_info[key]['degree']
        if degree == 1:
            degree_word = 'первой'
        elif degree == 2:
            degree_word = 'второй'
        elif degree == 3:
            degree_word = 'третьей'
        else:
            degree_word = degree
        img = Image.open(f"graphics\\{value['name_y']}.png")
        idraw = ImageDraw.Draw(img)
        font = ImageFont.truetype("arial.ttf", size=100)
        idraw.text((900, 5), f"Параметр: {value['name_y']}\n"
                             f"Алгоритм: {key.split('{')[0]}\n"
                              f"Зависимость {degree_word} степени\n"
                           f"Метрики:\n"
                           f"\tmae:  {value['mae']}\n"
                              f"\tmse:  {value['mse']}\n"
                              f"\trmse: {value['rmse']}\n"
                             f"Оптимизировалась: {pseven_info['metric']}", font=font, fill='black')
        img.save(f"graphics\\{value['name_y']}.png")
