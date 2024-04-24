import dash
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import fiona
import geopandas as gpd
from shapely.geometry import Point, Polygon, mapping
from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from statistics import mean

#Carregando os dados e gerando o data frame 
dfdengue = pd.read_csv("dengue_1-14.csv")
dfcasos = pd.DataFrame()
dfcasos ['Data'] = dfdengue['data_iniSE']
dfcasos ['Casos'] = dfdengue['casos']
dfcasos ['Temperatura'] = dfdengue['tempmed']
dfcasos ['Umidade']= dfdengue['umidmed']
dfcasos = dfcasos.sort_index(ascending=False)

# Importar dados do geojson

mp_bairro = gpd.read_file('BAIRROS+GUARAREMA.geojson')

# Adicionando coluna casos de dengue

dengue = [4, 0, 2, 2, 2, 5, 4, 5, 4, 0, 4, 0, 2, 2, 2, 2, 4, 4, 4, 4, 5, 5, 4, 0, 2, 0, 5, 0, 4, 2, 2, 4, 0, 2, 0, 0, 2, 4, 2]

# Transformar casos em index

mp_bairro['Casos']= dengue
mp_bairro.index = list(mp_bairro['name'])

# Gerando o mapa de Guararema

fig_map = px.choropleth_mapbox(mp_bairro,
    geojson=mp_bairro.geometry,
    locations=mp_bairro.index,
    color_continuous_scale= 'reds',
    color="Casos",
    opacity=0.5,
    center = {"lat": (((mean(list(mp_bairro.geometry.bounds.maxy))-mean(list(mp_bairro.geometry.bounds.miny)))/2)+mean(list(mp_bairro.geometry.bounds.miny)))
    , "lon": (((mean(list(mp_bairro.geometry.bounds.maxx))-mean(list(mp_bairro.geometry.bounds.minx)))/2)+mean(list(mp_bairro.geometry.bounds.minx)))},
    #center={"lat": -23.4126, "lon": -46.0411},
    labels={'index':'Bairro'},
    mapbox_style="carto-positron",
    zoom=10,
)

fig_map.update_layout(margin=dict(l=1, r=1, t=1, b=1))

# Gerando os graficos a serem exibidos
    
fig_cas = px.line(dfcasos, x='Data', y="Casos", markers=True)
fig_temp = px.line(dfcasos, x='Data', y="Temperatura", markers=True, title='Temperatura')
fig_umid = px.line(dfcasos, x='Data', y="Umidade", markers=True, title='Umidade')

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout = dbc.Container(
    [
        dcc.Store(id="store"),
        html.H1(children='Monitora Dengue Guararema'),
        html.Hr(),
        html.H2(children='Informações sobre casos de Dengue em Guararema'),
        html.Hr(),
               dbc.Tabs(
            [
                dbc.Tab(label="Casos de Dengue", tab_id="casos"),
                dbc.Tab(label="Clima", tab_id="clima"),
                dbc.Tab(label="Mapa de casos", tab_id="mapa")
            ],
            id="tabs",
            active_tab="casos",
        ),
        html.Div(id="tab-content", className="p-4"),
    ]
)

@app.callback(
    Output("tab-content", "children"),
    [Input("tabs", "active_tab"), Input("store", "data")],
)
def render_tab_content(active_tab, data):

    # Definindo abas ativas
    if active_tab == "casos":
        return dcc.Graph(figure=fig_cas)
    elif active_tab == "clima":
        return dbc.Row(
            [
                dbc.Col(dcc.Graph(figure=fig_temp)),
                dbc.Col(dcc.Graph(figure= fig_umid)),
            ]
        )
    elif active_tab == "mapa":
        return dcc.Graph(figure=fig_map)
    
    
if __name__ == '__main__':
    app.run_server(debug=True, port=8888)