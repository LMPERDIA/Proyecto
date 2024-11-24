import dash
from dash import Dash, html, dcc

# Inicializar la aplicación
app = Dash(__name__, use_pages=True)
app.title = "Proyecto Final Despliegue"

# Diseño principal
app.layout = html.Div(
    children=[
        html.Div(
            [
                html.Nav(
                    children=[
                        dcc.Link("Portada", href="/", style={"margin": "10px"}),
                        dcc.Link("Formulario", href="/formulario", style={"margin": "10px"}),
                        dcc.Link("Historico", href="/visualizaciones", style={"margin": "10px"}),
                    ],
                    style={"textAlign": "center", "marginBottom": "20px"},
                ),
            ]
        ),
        dash.page_container  # Contenedor donde se muestran las páginas
    ],
    style={
        "backgroundColor": "#FFFBF0",  # Color de fondo (gris oscuro en este caso)
        "color": "#9B005B",  # Color del texto por defecto
        "minHeight": "100vh",  # Asegurar que ocupe toda la altura de la pantalla
        "padding": "20px",  # Espaciado alrededor del contenido
    }
)

if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0', port=8050)