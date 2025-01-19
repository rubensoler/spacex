import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Cargar datos
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# Obtener nombres únicos de los sitios de lanzamiento
launch_sites = spacex_df['Launch Site'].unique().tolist()

# Crear las opciones del dropdown con la opción "All Sites"
dropdown_options = [{'label': 'All Sites', 'value': 'ALL'}] + \
                   [{'label': site, 'value': site} for site in launch_sites]

# Crear la aplicación Dash
app = dash.Dash(__name__)

# Layout de la aplicación
app.layout = html.Div([
    html.H1(
        "SpaceX Launch Records Dashboard",
        style={"textAlign": "center", "color": "#503D36", "font-size": "40px"}
    ),
    # Dropdown para seleccionar sitios de lanzamiento
    dcc.Dropdown(
        id='site-dropdown',
        options=dropdown_options,
        value='ALL',
        placeholder="Select a Launch Site here",
        searchable=True
    ),
    html.Br(),
    # Gráfico de pie
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),
    # Slider de rango de carga útil
    html.P("Payload range (Kg):"),
    dcc.RangeSlider(
        id='payload-slider',
        min=0, max=10000, step=1000,
        marks={i: str(i) for i in range(0, 10001, 1000)},
        value=[0, 10000]
    ),
    html.Br(),
    # Gráfico de dispersión
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# Callback para actualizar el gráfico de pie
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(
            spacex_df,
            names='class',
            title='Total Success Launches for All Sites',
            hole=0.3
        )
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.pie(
            filtered_df,
            names='class',
            title=f'Total Success Launches for {entered_site}',
            hole=0.3
        )
    return fig

# Callback para actualizar el gráfico de dispersión
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_scatter_chart(entered_site, payload_range):
    low, high = payload_range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & 
                            (spacex_df['Payload Mass (kg)'] <= high)]
    if entered_site == 'ALL':
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)', y='class',
            color='Booster Version',
            title='Payload vs. Outcome for All Sites',
            labels={"class": "Launch Outcome"}
        )
    else:
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)', y='class',
            color='Booster Version',
            title=f'Payload vs. Outcome for {entered_site}',
            labels={"class": "Launch Outcome"}
        )
    return fig

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)
