import dash
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

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
    
    #Carregando os dados e gerando o data frame 
    dfdengue = pd.read_csv("dengue_1-14.csv")
    dfcasos = pd.DataFrame()
    dfcasos ['Data'] = dfdengue['data_iniSE']
    dfcasos ['Casos'] = dfdengue['casos']
    dfcasos ['Temperatura'] = dfdengue['tempmed']
    dfcasos ['Umidade']= dfdengue['umidmed']
    dfcasos = dfcasos.sort_index(ascending=False)


    # Gerando os graficos a serem exibidos
    
    fig_cas = px.line(dfcasos, x='Data', y="Casos", markers=True)
    fig_temp = px.line(dfcasos, x='Data', y="Temperatura", markers=True, title='Temperatura')
    fig_umid = px.line(dfcasos, x='Data', y="Umidade", markers=True, title='Umidade')

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

if __name__ == '__main__':
    app.run_server(debug=True, port=8888)