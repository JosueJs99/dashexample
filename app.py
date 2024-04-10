from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
dfdengue = pd.read_csv("dengue_1-14.csv")
dfcasos = pd.DataFrame()
sem = []
cont = len(dfdengue)
for c in range(0, 13):
    sem += cont,
    cont -= 1
dfcasos ['Semanas'] = sem
dfcasos ['Casos'] = dfdengue['casos']
dfcasos ['Temperatura'] = dfdengue['tempmed']
dfcasos ['Umidade']= dfdengue['umidmed']
dfcasos = dfcasos.sort_index(ascending=False)


opcoes = list(dfcasos['Semanas'])
opcoes.append("Todas as semanas")

fig_cas = px.line(dfcasos, x='Semanas', y="Casos", markers=True, title='Casos de Dengue')
fig_temp = px.line(dfcasos, x='Semanas', y="Temperatura", markers=True, title='Temperatura')
fig_umid = px.line(dfcasos, x='Semanas', y="Umidade", markers=True, title='Umidade')


app.layout = html.Div(children=[
    html.H1(children='Monitora Dengue Guararema'),
    html.H2(children='Informações sobre casos de Dengue em Guararema'),

    html.Div(children='''
        Obs. Esse gráfico mostra o número de casos de dengue por semana em 2024.
    '''),

    dcc.Dropdown(opcoes, value='Todas as semanas', id='lista-semanas'),
    
    dcc.Graph(
        id='grafico_casos',
        figure=fig_cas
    ),
    dcc.Graph(
        id='grafico_temp',
        figure=fig_temp
    ),
    dcc.Graph(
        id='grafico_umid',
        figure=fig_umid
    )
])

if __name__ == '__main__':
    app.run(debug=True)