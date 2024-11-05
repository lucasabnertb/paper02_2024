import pandas as pd
import os

import pandas as pd

def media_de_publico(df, ano):
    # Filtra o DataFrame para o ano específico
    df_filtrado = df[df['ano_campeonato'] == ano]
    
    # Agrupa os dados pelo time mandante e calcula a média de público
    media_publico = df_filtrado.groupby('time_mandante')['publico'].mean().reset_index()
    
    # Adiciona o ano ao DataFrame resultante
    media_publico['ano_campeonato'] = ano
    
    # Reorganiza as colunas
    media_publico = media_publico[['ano_campeonato', 'time_mandante', 'publico']]
    
    # Seleciona a maior média
    maior_media = media_publico.loc[media_publico['publico'].idxmax()]

    return media_publico, maior_media





def media_de_valor_equipe(df, ano):
    # Filtra o DataFrame para o ano específico
    df_filtrado = df[df['ano_campeonato'] == ano]
    
    # Calcula o maior valor das equipes mandantes e visitantes
    maior_valor_mandante = df_filtrado.groupby('time_mandante')['valor_equipe_titular_mandante'].max().reset_index()
    maior_valor_visitante = df_filtrado.groupby('time_visitante')['valor_equipe_titular_visitante'].max().reset_index()
    
    # Renomeia as colunas para facilitar a junção
    maior_valor_mandante.columns = ['time_mandante', 'maior_valor_mandante']
    maior_valor_visitante.columns = ['time_visitante', 'maior_valor_visitante']
    
    # Junta os DataFrames
    media = pd.merge(maior_valor_mandante, maior_valor_visitante, left_on='time_mandante', right_on='time_visitante', how='outer')
    
    # Calcula a média total
    media['media_total'] = (media['maior_valor_mandante'].fillna(0) + media['maior_valor_visitante'].fillna(0)) / 14
    
    # Adiciona o ano ao DataFrame resultante
    media['ano_campeonato'] = ano
    
    # Seleciona a maior média
    maior_media = media.loc[media['media_total'].idxmax()]

    # Reorganiza as colunas
    return media[['ano_campeonato', 'time_mandante', 'media_total']], maior_media
