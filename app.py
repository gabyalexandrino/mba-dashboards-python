import dash
from dash import html, dcc, Input, Output
import plotly.express as px
import pandas as pd

# Carrega o conjunto de dados
df_tips = px.data.tips()
app = dash.Dash(__name__)


# Define a estrutura da pagina.
# A palavra 'className' foi usada para aplicar estilos do arquivo 'style.css'
app.layout = html.Div(
    [
        html.H1("Dashboard de Analise de Gorjetas", className='h1'),

        html.Div(
            [
                # Coluna com os filtros
                html.Div(
                    [
                        html.Label("Escolha o Dia da Semana:", className='dropdown'),
                        dcc.Dropdown(
                            id='dropdown-dia',
                            options=[{'label': dia, 'value': dia} for dia in df_tips['day'].unique()] +
                                    [{'label': 'Todos', 'value': 'Todos'}],
                            value='Todos',
                            clearable=False
                        )
                    ],
                    className='coluna-filtros'
                ),

                # Coluna com os graficos
                html.Div(
                    [
                        dcc.Graph(id='grafico-gorjetas'),
                        dcc.Graph(id='grafico-contas'),
                        dcc.Graph(id='grafico-fumantes')
                    ],
                    className='coluna-graficos'
                )
            ],
            className='main'
        )
    ]
)


# Funcao que atualiza os graficos toda vez que o usuario mudar o filtro
@app.callback(
    [
        Output('grafico-gorjetas', 'figure'),
        Output('grafico-contas', 'figure'),
        Output('grafico-fumantes', 'figure')
    ],
    [
        Input('dropdown-dia', 'value')
    ]
)
def atualizar_dashboard(dia_selecionado):
    # Filtra o df com base na escolha do usuario
    if dia_selecionado == 'Todos':
        df_filtrado = df_tips
    else:
        df_filtrado = df_tips[df_tips['day'] == dia_selecionado]

    # Graficos
    # Relacao entre gorjeta x valor total da conta (boxplot)
    fig_gorjetas = px.box(
        df_filtrado, 
        x="day", 
        y="tip",
        title=f"Distribuicao das gorjetas - {dia_selecionado}"
    )

    # Distribuiçao do total da conta (histograma)
    fig_contas = px.histogram(
        df_filtrado, 
        x="total_bill", 
        color="sex",
        title=f"Distribuicao do total da conta - {dia_selecionado}"
    )

    # Proporcao de fumantes e não-fumantes (grafico de pizza)
    contagem_fumantes = df_filtrado['smoker'].value_counts().reset_index()
    contagem_fumantes.columns = ['smoker', 'count']
    fig_fumantes = px.pie(
        contagem_fumantes,
        values='count',
        names='smoker',
        title=f"Distribuicao de fumantes - {dia_selecionado}"
    )

    # A funcao retorna os graficos para serem exibidos
    return fig_gorjetas, fig_contas, fig_fumantes


# Executa a aplicacao
if __name__ == '__main__':
    app.run(port=8051, debug=True)
