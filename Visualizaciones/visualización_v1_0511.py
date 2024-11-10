# -*- coding: utf-8 -*-
"""Visualización_V1_0511.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1KlUlfDJ5LBc8jmhHZw1f7Xq97de8yUrO
"""

import pandas as pd

# Reemplaza 'ruta/del/archivo.csv' con la ubicación de tu archivo CSV
data = pd.read_csv('diamonds.csv')

# Muestra las primeras filas para verificar la carga
print(data.head())

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.preprocessing import LabelEncoder

# Cargar el dataset

df = pd.DataFrame(data)

# Preprocesamiento de datos
# Codificar variables categóricas
label_encoders = {}
for column in ['cut', 'color', 'clarity']:
    le = LabelEncoder()
    df[column] = le.fit_transform(df[column])
    label_encoders[column] = le  # Guardar el codificador para su uso posterior

# Separar características y objetivo
X = df.drop(columns=['price'])
y = df['price']

# Dividir el conjunto de datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenar un modelo de regresión (Random Forest)
model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)

# Hacer predicciones
y_pred = model.predict(X_test)

# Evaluar el modelo
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
print("Mean Absolute Error:", mae)
print("Mean Squared Error:", mse)

#!pip install dash

import dash
from dash import dcc, html, Input, Output
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import plotly.express as px

# Cargar el dataset
data = pd.read_csv('diamonds.csv')
df = pd.DataFrame(data)

# Preprocesamiento de datos
label_encoders = {}
for column in ['cut', 'color', 'clarity']:
    le = LabelEncoder()
    df[column] = le.fit_transform(df[column])
    label_encoders[column] = le

# Separar características y objetivo
X = df.drop(columns=['price'])
y = df['price']

# Dividir el conjunto de datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenar el modelo de regresión
model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)

# Inicializar la aplicación Dash
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Tablero de Predicción de Precios de Diamantes", style={'text-align': 'center'}),

    # Sección de entrada de datos
    html.Div([
        html.Label("Carat"),
        dcc.Input(id="input-carat", type="number", placeholder="Peso en quilates", step=0.01),

        html.Label("Cut"),
        dcc.Dropdown(
            id="input-cut",
            options=[{'label': i, 'value': label_encoders['cut'].transform([i])[0]} for i in label_encoders['cut'].classes_],
            placeholder="Seleccione el corte"
        ),

        html.Label("Color"),
        dcc.Dropdown(
            id="input-color",
            options=[{'label': i, 'value': label_encoders['color'].transform([i])[0]} for i in label_encoders['color'].classes_],
            placeholder="Seleccione el color"
        ),

        html.Label("Clarity"),
        dcc.Dropdown(
            id="input-clarity",
            options=[{'label': i, 'value': label_encoders['clarity'].transform([i])[0]} for i in label_encoders['clarity'].classes_],
            placeholder="Seleccione la claridad"
        ),

        html.Button("Predecir Precio", id="predict-button", n_clicks=0),
    ], style={'padding': '20px'}),

    # Mostrar predicción de precio
    html.Div(id="output-price", style={'font-size': '24px', 'text-align': 'center'}),

    # Gráficos de visualización de datos
    html.Div([
        dcc.Graph(id="scatter-plot", figure={}),
        dcc.Graph(id="box-plot", figure={})
    ])
])

# Callback para la predicción
@app.callback(
    Output("output-price", "children"),
    Input("predict-button", "n_clicks"),
    [
        Input("input-carat", "value"),
        Input("input-cut", "value"),
        Input("input-color", "value"),
        Input("input-clarity", "value")
    ]
)
def predict_price(n_clicks, carat, cut, color, clarity):
    if n_clicks > 0:
        # Realizar predicción con el modelo
        features = [[carat, cut, color, clarity, 61, 55, 4, 4, 2]]  # valores de ejemplo para depth, table, x, y, z
        predicted_price = model.predict(features)[0]
        return f"Precio estimado: ${predicted_price:.2f} USD"
    return "Ingrese los valores para obtener el precio"

# Callback para los gráficos
@app.callback(
    [Output("scatter-plot", "figure"), Output("box-plot", "figure")],
    Input("predict-button", "n_clicks")
)
def update_charts(n_clicks):
    # Gráfico de dispersión de carat vs precio
    scatter_fig = px.scatter(df, x="carat", y="price", title="Precio vs Carat")

    # Gráfico de caja para distribución de precios por claridad
    box_fig = px.box(df, x="clarity", y="price", title="Distribución de Precio por Claridad")

    return scatter_fig, box_fig

if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0', port=8050)