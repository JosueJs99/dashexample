import dash
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import fiona
import geopandas as gpd
import plotly.graph_objects as go
from dash import Dash, html, dcc, Input, Output
from shapely.geometry import Point, Polygon, mapping
from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from statistics import mean
from plotly.subplots import make_subplots

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

dengue = [4, 0, 2, 2, 2, 5, 4, 5, 4, 0, 4, 0, 2, 2, 2, 2, 4, 4, 4, 4,
          5, 5, 4, 0, 2, 0, 5, 0, 4, 2, 2, 4, 0, 2, 0, 0, 2, 4, 2]

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

# Gráfico relação entre Dengue e Temperatura

fig_dvst = make_subplots(specs=[[{"secondary_y": True}]])
# Casos de dengue
fig_dvst.add_trace(go.Scatter(x = dfcasos['Data'], y = dfcasos["Casos"], name = 'Casos de Dengue'))
# Temperatura
fig_dvst.add_trace(go.Scatter(x = dfcasos['Data'], y = dfcasos["Temperatura"], name = 'Temperatura Média'),
              secondary_y=True
              )

fig_dvst.update_layout(title='Relação entre Dengue e Temperatura',
xaxis_title='Semanas',
yaxis_title='Casos',
plot_bgcolor = 'white',
font = {'family': 'Arial','size': 16,'color': 'black'},
colorway=px.colors.qualitative.Set1)
fig_dvst.update_xaxes( showgrid=True, gridwidth=1, gridcolor='lightgray',
showline=True, linewidth=1, linecolor='black')
fig_dvst.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray',
showline=True, linewidth=1, linecolor='black')

# Gráfico relação entre Dengue e Umidade


fig_dvsu = make_subplots(specs=[[{"secondary_y": True}]])
# Casos de dengue
fig_dvsu.add_trace(go.Scatter(x = dfcasos['Data'], y = dfcasos["Casos"], name = 'Casos de Dengue'))
# Umidade
fig_dvsu.add_trace(go.Scatter(x = dfcasos['Data'], y = dfcasos["Umidade"], name = 'Umidade média'),
             secondary_y=True
              )

fig_dvsu.update_layout(title='Relação entre Dengue e Umidade',
xaxis_title='Semanas',
yaxis_title='Casos',
plot_bgcolor = 'white',
font = {'family': 'Arial','size': 16,'color': 'black'},
colorway=px.colors.qualitative.Light24)
fig_dvsu.update_xaxes( showgrid=True, gridwidth=1, gridcolor='lightgray',
showline=True, linewidth=1, linecolor='black')
fig_dvsu.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray',
showline=True, linewidth=1, linecolor='black')

# Material educativo

video_dengue = "/assets/dengue.mp4"
video_ciclo = "/assets/ciclo.mp4"
video_atividade = "/assets/atividade.mp4"
video_locais = "/assets/locais.mp4"
video_prevencao = "/assets/prevencao.mp4"
video_sintomas = "/assets/sintomas.mp4"

info1 = html.P(children='Fonte: http://educapes.capes.gov.br/handle/capes/585169', className="card-title")

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout = dbc.Container(
    [
        dcc.Store(id="store"),
        html.Br(),
        dbc.Card(
            dbc.CardBody(
                [
                html.H1(children='Monitora Dengue Guararema'),
                html.Br(),
                html.H2(children='Informações sobre casos de Dengue em Guararema'),
                ]
            )
        ),
        html.Br(),
        dbc.Card(
               dbc.Tabs(
            [
                dbc.Tab(label="Dengue e Temperatura", tab_id="d_vs_t", active_tab_class_name="active"),
                dbc.Tab(label="Dengue e Umidade", tab_id="d_vs_u"),
                dbc.Tab(label="Mapa de casos", tab_id="mapa")
            ],
            id="tabs",
            active_tab="casos",
                ),
        ),
        
        html.Div(id="tab-content", className="p-4"),
        
        html.Div(
            [
                dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                html.H2(children='Dengue e Origem', className="card-title"),
                                html.Br(),
                                html.Video(
                                    controls = True,
                                    id = 'movie_player_1',
                                    src = video_dengue,
                                    autoPlay=True,
                                    muted=True,
                                    loop=True,
                                    width=560, height=315,
                                ),
                                html.P(children='Fonte: http://educapes.capes.gov.br/handle/capes/585169', className="card-title")
                                ]
                            ),
                            style={"width": "37rem"},
                        ),
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                html.H2(children='Ciclo de Vida do Mosquito', className="card-title"),
                                html.Br(),
                                html.Video(
                                    controls = True,
                                    id = 'movie_player_2',
                                    src = video_ciclo,
                                    autoPlay=True,
                                    muted=True,
                                    loop=True,
                                    width=560, height=315
                                ),
                                html.P(children='Fonte: http://educapes.capes.gov.br/handle/capes/585169', className="card-title")
                                ]
                            ),
                            style={"width": "37rem"},
                        ),
                    ),
                ]
                ),
                html.Br(),
                dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                html.H2(children='Atividades do Mosquito', className="card-title"),
                                html.Br(),
                                html.Video(
                                    controls = True,
                                    id = 'movie_player_3',
                                    src = video_atividade,
                                    autoPlay=True,
                                    muted=True,
                                    loop=True,
                                    width=560, height=315
                                ),
                                html.P(children='Fonte: http://educapes.capes.gov.br/handle/capes/585169', className="card-title")
                                ]
                            ),
                            style={"width": "37rem"},
                        ),
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                html.H2(children='Locais de proliferação', className="card-title"),
                                html.Br(),
                                html.Video(
                                    controls = True,
                                    id = 'movie_player_4',
                                    src = video_locais,
                                    autoPlay=True,
                                    muted=True,
                                    loop=True,
                                    width=560, height=315
                                ),
                                html.P(children='Fonte: http://educapes.capes.gov.br/handle/capes/585169', className="card-title")
                                ]
                            ),
                            style={"width": "37rem"},
                        ),
                   
                    ),
                ]
                ),
                html.Br(),
                dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                html.H2(children='Formas de Prevenção', className="card-title"),
                                html.Br(),
                                html.Video(
                                    controls = True,
                                    id = 'movie_player_5',
                                    src = video_prevencao,
                                    autoPlay=True,
                                    muted=True,
                                    loop=True,
                                    width=560, height=315
                                ),
                                html.P(children='Fonte: http://educapes.capes.gov.br/handle/capes/585169', className="card-title")
                                ]
                            ),
                            style={"width": "37rem"},
                        ),
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                html.H2(children='Sintomas da Dengue e Orientações', className="card-title"),
                                html.Br(),
                                html.Video(
                                    controls = True,
                                    id = 'movie_player_6',
                                    src = video_sintomas,
                                    autoPlay=True,
                                    muted=True,
                                    loop=True,
                                    width=560, height=315
                                ),
                                html.P(children='Fonte: http://educapes.capes.gov.br/handle/capes/585169', className="card-title")
                                ]
                            ),
                            style={"width": "37rem"},
                        ),
                    ),
                ]
                ),
            ],
        ),
        html.Br()   
    ]
)
              

@app.callback(
    Output("tab-content", "children"),
    [Input("tabs", "active_tab"), Input("store", "data")],
)
def render_tab_content(active_tab, data):

    # Definindo abas ativas
    if active_tab == "d_vs_t":
        return dbc.Card(dcc.Graph(figure=fig_dvst))
    elif active_tab == "d_vs_u":
        return dbc.Card(dcc.Graph(figure= fig_dvsu))
    elif active_tab == "mapa":
        return dbc.Card(dcc.Graph(figure=fig_map))
    
    
if __name__ == '__main__':
    app.run_server(debug=True, port=8888)