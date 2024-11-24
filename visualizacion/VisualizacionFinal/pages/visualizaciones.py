from dash import html, dcc, Input, Output, State, register_page, callback
import requests
import pandas as pd
import plotly.express as px

# Registrar la página
register_page(__name__, path="/visualizaciones")

# Cargar el dataset y entrenar el modelo
data = pd.read_csv('./data/diamonds.csv')
df = pd.DataFrame(data)

layout = html.Div([
    # Resumen de datos históricos (Sección 3)
    html.Div([
        html.H3("Resumen de datos históricos", style={'text-align': 'center'}),
        dcc.Graph(id="scatter-plot", figure={}, style={'display': 'inline-block', 'width': '48%'}),
        dcc.Graph(id="box-plot", figure={}, style={'display': 'inline-block', 'width': '48%'})
    ])
    ]
)

# Callback para los gráficos
@callback(
    [Output("scatter-plot", "figure"), Output("box-plot", "figure")],
    Input("scatter-plot", "id")  # Se puede usar cualquier Input dummy para inicializar
)
def update_charts(_):
    scatter_fig = px.scatter(df, x="carat", y="price", title="Precio vs Carat")
    box_fig = px.box(df, x="clarity", y="price", title="Distribución de Precio por Claridad")
    return scatter_fig, box_fig