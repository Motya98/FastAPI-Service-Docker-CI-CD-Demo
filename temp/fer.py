import pickle
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_absolute_error, mean_squared_error
with open(r"C:\Users\barha\PycharmProjects\Machine Learning\models\Ridge{alpha0.0001max_iter1000000}_Degree2_mass.pkl",
          'rb') as file:
    model = pickle.load(file)
df = pd.read_csv(r"C:\Users\barha\PycharmProjects\Machine Learning\data2.csv")
x_test = df[df.columns[0:4:1]]
poly = PolynomialFeatures(degree=2)
poly.fit(x_test)
x_test = poly.transform(x_test)
scaler = StandardScaler()
scaler.fit(x_test)
x_test = scaler.transform(x_test)
y_test = df[df.columns[4]]
y_pred = model.predict(x_test)

print(mean_absolute_error(y_test, y_pred))

print(model)