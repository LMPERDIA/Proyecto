from dash import html, dcc, Input, Output, State, register_page

# Registrar la página
register_page(__name__, path="/")

layout = html.Div([
    # Portada
    html.Div([
        html.H1("VALDI", style={'text-align': 'center', 'font-size': '48px', 'fontfamily':'Impact'}),
        html.Div(
            children=[
                html.Img(
                    src="/assets/ImagenInicial.jpeg",  # Ruta de la imagen
                    style={
                        "display": "block",
                        "margin": "auto",
                        "width": "50%",
                        "height": "auto",  # Mantener altura original
                    },
                ),
            ],
            style={"textAlign": "center", "marginTop": "20px"},
        ),
        html.H2("VALuador de Diamantes Inteligente", style={'text-align': 'center', 'font-size': '24px', 'fontfamily':'Impact'})
        ]),
    ]
)