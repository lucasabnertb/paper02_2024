from functions import *
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
import datetime
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.grid import grid
from streamlit_extras.tags import tagger_component
import openai


# Carregar as variáveis do arquivo .env
load_dotenv()

# Define a página para usar a largura total
st.set_page_config(layout="wide")

# Configurações do banco de dados a partir das variáveis de ambiente
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
database = os.getenv('DB_DATABASE')
schema = os.getenv('DB_SCHEMA')
table_name = os.getenv('DB_TABLE')

# Criação da string de conexão
connection_string = f"mysql+mysqlconnector://{user}:{password}@{host}/{database}"
engine = create_engine(connection_string)

# Consulta para obter dados de campeões e anos
df = pd.read_sql_query(
    """
    SELECT b.*, vc.campeao
    FROM dataplace.brasileirao b
    LEFT JOIN dataplace.vw_campeoes vc ON b.ano_campeonato = vc.ano_campeonato;
    """, engine
)

# Consulta para obter dados de média de público por ano
df_publico = pd.read_sql_query("SELECT ano_campeonato, media_de_publico FROM dataplace.vw_media_publico;", engine)

# Consulta para obter os anos disponíveis
edicao = pd.read_sql_query(f"SELECT DISTINCT ano_campeonato FROM {schema}.{table_name};", engine)

def build_sidebar():
    st.image("C:/Users/Lucas/Desktop/papper/app/image/logo.png", width=250)
    ano = st.multiselect(label="Edição", options=edicao['ano_campeonato'], placeholder="Edição")
    return ano

# Estilo de fonte
st.markdown(
    """
    <style>
    .small-font {
        font-size: 18px; /* Ajuste o tamanho da fonte aqui */
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Função para plotar o gráfico de barras com Plotly


# Exemplo de função substituída usando st.bar_chart
# Função para plotar o gráfico com rótulos usando Plotly
def plotar_grafico_media_publico():
    # Converte os dados para o formato adequado para exibir rótulos
    rótulos_formatados = df_publico['media_de_publico'].astype(int).astype(str)
    
    # Configura o gráfico com Plotly Express
    fig = px.bar(
        df_publico, 
        x='ano_campeonato', 
        y='media_de_publico', 
        title='Média de Público por Ano',
        color_discrete_sequence=['#F7B401']
    )
    
    # Adiciona rótulos de dados formatados
    fig.update_traces(text=rótulos_formatados, textposition='auto')
    
    # Ajusta os rótulos dos eixos
    fig.update_layout(xaxis_title="Ano do Campeonato", yaxis_title="Média de Público")
    
    # Exibe o gráfico no Streamlit
    st.plotly_chart(fig, use_container_width=True)


# Configura sua chave da API
openai.api_key = os.getenv('OPENAI_API_KEY')

def consultar_openai(prompt):
    try:
        # Faz a solicitação à API com limite de tokens
        resposta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # ou outro modelo que você deseja usar
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=500  # Limita a resposta a 200 tokens
        )

        # Extrai o texto da resposta
        texto_resposta = resposta['choices'][0]['message']['content']
        return texto_resposta

    except Exception as e:
        return f"Ocorreu um erro: {str(e)}"


def exibir_valores_selecionados(ano):
    mygrid = grid(3, vertical_align="top")

    for e in ano:
           
        # Filtra o campeão para o ano selecionado
        dados_ano = df[df['ano_campeonato'] == e]
        
        # Verifica se existe um registro para o ano selecionado
        if not dados_ano.empty:
            nome_campeao = dados_ano['campeao'].values[0]
        else:
            nome_campeao = "Não disponível"

        # Cria o container e insere os dados
        c = mygrid.container(border=True)
        c.subheader(f"Campeão {e}", divider='grey')
        colA, colB = c.columns(2)
        
        # Exibe a imagem e o nome do campeão com tamanho de fonte menor
        colA.image(f'C:/Users/Lucas/Desktop/papper/app/image/{nome_campeao}.png', width=50)
        colB.markdown(f"<p class='small-font'>Equipe: {nome_campeao}</p>", unsafe_allow_html=True)

        media_publico, maior_media = media_de_publico(df,e)
        media_publico_ano = maior_media['publico'].astype(int).astype(str)
        time_media_publico_ano = maior_media['time_mandante']

        # Cria o container e insere os dados
        c = mygrid.container(border=True)
        c.subheader(f"Maior Média de Público", divider='grey')
        colC, colD = c.columns(2)
        
        # Exibe a imagem e o nome do campeão com tamanho de fonte menor
        colC.image(f'C:/Users/Lucas/Desktop/papper/app/image/{time_media_publico_ano}.png', width=50)
        colD.markdown(f"<p class='small-font'>{time_media_publico_ano}: {media_publico_ano}</p>", unsafe_allow_html=True)

        # Chama a função para obter as médias
        media_valor_equipe, time_mais_valioso = media_de_valor_equipe(df, e)

        media_valor_equipe_final = round(time_mais_valioso['media_total'],2)
        
        # Obtém o nome do time mais valioso
        nome_time_mais_valioso = time_mais_valioso['time_mandante']

        # Cria o container e insere os dados
        c = mygrid.container(border=True)
        c.subheader(f"Time mais valioso", divider='grey')
        colE, colF = c.columns(2)
        
        # Exibe a imagem e o nome do campeão com tamanho de fonte menor
        colE.image(f'C:/Users/Lucas/Desktop/papper/app/image/{nome_time_mais_valioso}.png', width=50)
        colF.markdown(f"<p class='small-font'>{nome_time_mais_valioso}: {media_valor_equipe_final}</p>", unsafe_allow_html=True)

        st.subheader(f"Edição : {e}",divider='grey')
        # Exibe o gráfico de média de público


        # Prompt embutido no código para engenharia de prompts
        prompt = f'''Considere os dados contidos no dataset {dados_ano} retorne a seguinte lista de solicitações.
        1 - Retorne Qual time foi campeão, considere os dados do dataset {dados_ano['campeao']}
        2 - Considere a coluna {dados_ano['gols_mandante']} e informe Qual o time que fez mais gols como mandante ao longo do ano. Informe o número de gols.
        3 - Qual time possui a maior media de publico como mandante ao longo do ano (cite o nome do estadio e a média). 
        4 - Qual foi o maior placar e em qual confronto.
        5 - Qual foi o percentual de empates.
        Por fim retorne alguma curiosidade sobre os dados contidos no dataset {dados_ano}.
        Retorne apenas as respostas completas.'''

        resposta = consultar_openai(prompt)

        st.markdown(f"### Insights gerados usando a API da OpenAI:\n\n{resposta}")  


plotar_grafico_media_publico()

with st.sidebar:
    ano = build_sidebar()
    

if ano:
    exibir_valores_selecionados(ano)

