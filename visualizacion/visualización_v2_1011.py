# -*- coding: utf-8 -*-
"""visualización_v2_01011.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1XcXtfDePXV1_givTA5eiAVAxyX8NNf-1

Visualización Versión 2
"""

#!pip install dash

import dash
from dash import dcc, html, Input, Output
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import plotly.express as px
import requests

# Cargar el dataset y entrenar el modelo
data = pd.read_csv('diamonds.csv')
df = pd.DataFrame(data)

# Preprocesamiento de datos
label_encoders = {}
for column in ['cut', 'color', 'clarity']:
    le = LabelEncoder()
    df[column] = le.fit_transform(df[column])
    label_encoders[column] = le

X = df.drop(columns=['price'])
y = df['price']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)

# Inicializar la aplicación Dash
app = dash.Dash(__name__)

app.layout = html.Div([
    # Portada
    html.Div([
        html.H1("VALDI", style={'text-align': 'center', 'font-size': '48px', 'fontfamily':'Impact'}),
        html.H2("VALuador de Diamantes Inteligente", style={'text-align': 'center', 'font-size': '24px', 'fontfamily':'Impact'})
    ], style={'padding': '40px', 'background-color': '#f0f0f0'}),

    # Formulario de entrada de características (Sección 1)
    html.Div([
        html.H3("Ingrese las características del diamante", style={'text-align': 'center'}),

        html.Div([
        html.Label("Peso en quilates (Carat)"),
        dcc.Input(id="input-carat", type="number", placeholder="Peso en quilates", step=0.01)]
        ,style={'marginBottom': '20px'}),

        html.Div([
        html.Label("Total porcentaje de profundidad (depth)"),
        dcc.Input(id="input-depth", type="number", placeholder="43--79 %", step=0.01)]
        ,style={'marginBottom': '20px'}),

        html.Div([
        html.Label("Ancho del tope del diamante (table)"),
        dcc.Input(id="input-table", type="number", placeholder="43--79", step=0.01)]
        ,style={'marginBottom': '20px'}),

        html.Div([
        html.Label("Largo del diamante (X)"),
        dcc.Input(id="input-X", type="number", placeholder="milimetros", step=0.01)]
        ,style={'marginBottom': '20px'}),

        html.Div([
        html.Label("Ancho del diamante (Y)"),
        dcc.Input(id="input-Y", type="number", placeholder="milimetros", step=0.01)]
        ,style={'marginBottom': '20px'}),

        html.Div([
        html.Label("Profundidad del diamante (Z)"),
        dcc.Input(id="input-Z", type="number", placeholder="milimetros", step=0.01)]
        ,style={'marginBottom': '20px'}),

        html.Div([
        html.Label("Corte (Cut)"),
        dcc.Dropdown(
            id="input-cut",
            options=[{'label': 'Good', 'value': 'Good'},
                    {'label': 'Ideal', 'value': 'Ideal'},
                    {'label': 'Premium', 'value': 'Premium'},
                    {'label': 'Very Good', 'value': 'VeryGood'}],
            placeholder="Seleccione el corte")]
        ,style={'marginBottom': '20px'}),

        html.Div([
        html.Label("Color"),
        dcc.Dropdown(
            id="input-color",
            options=[{'label': 'Color E', 'value': 'E'},
                    {'label': 'Color F', 'value': 'F'},
                    {'label': 'Color G', 'value': 'G'},
                    {'label': 'Color H', 'value': 'H'},
                    {'label': 'Color I', 'value': 'I'},
                    {'label': 'Color J', 'value': 'J'}],
            placeholder="Seleccione el color")]
        ,style={'marginBottom': '20px'}),

        html.Div([
        html.Label("Claridad (Clarity)"),
        dcc.Dropdown(
            id="input-clarity",
            options=[{'label': 'Claridad IF', 'value': 'IF'},
                    {'label': 'Claridad SI1', 'value': 'SI1'},
                    {'label': 'Claridad SI2', 'value': 'SI2'},
                    {'label': 'Claridad VS1', 'value': 'VS1'},
                    {'label': 'Claridad VS2', 'value': 'VS2'},
                    {'label': 'Claridad VVS1', 'value': 'VVS1'},
                    {'label': 'Claridad VVS2', 'value': 'VVS2'}],
            placeholder="Seleccione la claridad")]
        ,style={'marginBottom': '20px'}),

        html.Button("Predecir Precio", id="predict-button", n_clicks=0, style={'margin-top': '20px'}),
    ], style={'width': '50%', 'margin': '0 auto', 'padding': '20px'}), #style={'padding': '20px', 'text-align': 'center'}),

    # Resultado de la predicción y características del diamante (Sección 2)
    html.Div(id="output-section", style={'padding': '20px', 'text-align': 'center', 'font-size': '24px'}),

    # Resumen de datos históricos (Sección 3)
    html.Div([
        html.H3("Resumen de datos históricos", style={'text-align': 'center'}),
        dcc.Graph(id="scatter-plot", figure={}, style={'display': 'inline-block', 'width': '48%'}),
        dcc.Graph(id="box-plot", figure={}, style={'display': 'inline-block', 'width': '48%'})
    ])
])

# Callback simplificado para la predicción de precios
@app.callback(
    Output("output-section", "children"),
    Input("predict-button", "n_clicks"),
    [
        Input("input-carat", "value"),
        Input("input-depth", "value"),
        Input("input-table", "value"),
        Input("input-X", "value"),
        Input("input-Y", "value"),
        Input("input-Z", "value"),
        Input("input-cut", "value"),
        Input("input-color", "value"),
        Input("input-clarity", "value")
    ]
)
def predict_price(n_clicks, carat, depth, table, X, Y, Z, cut, color, clarity):
    # Verifica que haya un clic y que todas las entradas no sean None
    if n_clicks > 0 and carat is not None and depth is not None and table is not None and X is not None and Y is not None and Z is not None and cut is not None and color is not None and clarity is not None:
        # Se transforman los datos para el modelo
        match cut:
            case 'Good':
                cutArray = [1,0,0,0]
            case 'Ideal':
                cutArray = [0,1,0,0]
            case 'Premium':
                cutArray = [0,0,1,0]
            case 'VeryGood':
                cutArray = [0,0,0,1]
        match color:
            case 'E':
                colorArray = [1,0,0,0,0,0]
            case 'F':
                colorArray = [0,1,0,0,0,0]
            case 'G':
                colorArray = [0,0,1,0,0,0]
            case 'H':
                colorArray = [0,0,0,1,0,0]
            case 'I':
                colorArray = [0,0,0,0,1,0]
            case 'J':
                colorArray = [0,0,0,0,0,1]
        match clarity:
            case 'IF':
                clarityArray = [1,0,0,0,0,0,0]
            case 'SI1':
                clarityArray = [0,1,0,0,0,0,0]
            case 'SI2':
                clarityArray = [0,0,1,0,0,0,0]
            case 'VS1':
                clarityArray = [0,0,0,1,0,0,0]
            case 'VS2':
                clarityArray = [0,0,0,0,1,0,0]
            case 'VVS1':
                clarityArray = [0,0,0,0,0,1,0]
            case 'VVS2':
                clarityArray = [0,0,0,0,0,0,1]
        try:
            # Intenta hacer la predicción
            features = list([carat, depth, table, X, Y, Z])
            features.extend(cutArray)
            features.extend(colorArray)
            features.extend(clarityArray)
            # Se hace la solicitud a la API
            headers_API = {'Content-Type': 'application/json'}
            data_API = {'features':[0.23, 61.5, 55.0, 326, 3.95, 3.98, 2.43, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1 ,1]}
            #predicted_price = model.predict(features)[0]
            predictedPrice = requests.post('http://54.86.72.39:8000/predict',headers=headers_API,json=data_API)
            predict = predictedPrice.json()['prediction'][0]
            # Devuelve la estructura HTML con el precio estimado y características
            return [
                html.H3("Predicción de Precio", style={'text-align': 'center'}),
                html.P(f"Precio estimado: ${predict:.2f} USD", style={'font-size': '32px', 'font-weight': 'bold'}),
                html.Hr(),
                html.H4("Características ingresadas"),
                html.P(f"Carat: {carat}, Cut: {cut}, Color: {color}, Clarity: {clarity}")
            ]
        except Exception as e:
            # En caso de error, devuelve el mensaje del error
            return f"Error en la predicción: {str(e)}"
    # Mensaje inicial si no se han ingresado valores
    return "Ingrese los valores para obtener el precio"


# Callback para los gráficos
@app.callback(
    [Output("scatter-plot", "figure"), Output("box-plot", "figure")],
    Input("predict-button", "n_clicks")
)
def update_charts(n_clicks):
    scatter_fig = px.scatter(df, x="carat", y="price", title="Precio vs Carat")
    box_fig = px.box(df, x="clarity", y="price", title="Distribución de Precio por Claridad")
    return scatter_fig, box_fig

if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0', port=8050)