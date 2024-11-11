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
        html.H1("VALDI", style={'text-align': 'center', 'font-size': '48px'}),
        html.H2("Valuador de Diamantes Inteligente", style={'text-align': 'center', 'font-size': '24px'})
    ], style={'padding': '40px', 'background-color': '#f0f0f0'}),

    # Formulario de entrada de características (Sección 1)
    html.Div([
        html.H3("Ingrese las características del diamante", style={'text-align': 'center'}),
        html.Label("Peso en quilates (Carat)"),
        dcc.Input(id="input-carat", type="number", placeholder="Peso en quilates", step=0.01),

        html.Label("Corte (Cut)"),
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

        html.Label("Claridad (Clarity)"),
        dcc.Dropdown(
            id="input-clarity",
            options=[{'label': i, 'value': label_encoders['clarity'].transform([i])[0]} for i in label_encoders['clarity'].classes_],
            placeholder="Seleccione la claridad"
        ),

        html.Button("Predecir Precio", id="predict-button", n_clicks=0, style={'margin-top': '20px'}),
    ], style={'padding': '20px', 'text-align': 'center'}),

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
        Input("input-cut", "value"),
        Input("input-color", "value"),
        Input("input-clarity", "value")
    ]
)
def predict_price(n_clicks, carat, cut, color, clarity):
    # Verifica que haya un clic y que todas las entradas no sean None
    if n_clicks > 0 and carat is not None and cut is not None and color is not None and clarity is not None:
        try:
            # Intenta hacer la predicción
            features = [[carat, cut, color, clarity, 61, 55, 4, 4, 2]]
            predicted_price = model.predict(features)[0]
            # Devuelve la estructura HTML con el precio estimado y características
            return [
                html.H3("Predicción de Precio", style={'text-align': 'center'}),
                html.P(f"Precio estimado: ${predicted_price:.2f} USD", style={'font-size': '32px', 'font-weight': 'bold'}),
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