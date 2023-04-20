#bibliotecas

import pandas as pd
import numpy as np
import plotly.express as px
import folium
import streamlit_folium
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static

#configuração da página
st.set_page_config(
    page_title="Cidades",
    layout = "wide"
)

#aplicando funções padrão

# Renomear as colunas do DataFrame
def rename_columns(dataframe):
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    return df

#Preenchimento do nome dos países
COUNTRIES = {
    1: "India",
    14: "Australia",
    30: "Brazil",
    37: "Canada",
    94: "Indonesia",
    148: "New Zeland",
    162: "Philippines",
    166: "Qatar",
    184: "Singapure",
    189: "South Africa",
    191: "Sri Lanka",
    208: "Turkey",
    214: "United Arab Emirates",
    215: "England",
    216: "United States of America",
    }
def country_name(country_id):
    return COUNTRIES[country_id]

#Criação do nome das Cores
COLORS = {
    "3F7E00": "darkgreen",
    "5BA829": "green",
    "9ACD32": "lightgreen",
    "CDD614": "orange",
    "FFBA00": "red",
    "CBCBC8": "darkred",
    "FF7800": "darkred",
    }

def color_name(color_code):
    return COLORS[color_code]

#limpeza do arquivo
def clean_code(df):
    filtros = (( df["Restaurant ID"] != "nan") &
               ( df["Restaurant Name"] != "nan") &
               ( df["Country Code"] != "nan") &
               ( df["City"] != "nan") &
               ( df["Address"] != "nan") &
               ( df["Locality"] != "nan") &
               ( df["Locality Verbose"] != "nan") &
               ( df["Longitude"] != "nan") &
               ( df["Latitude"] != "nan") &
               ( df["Cuisines"] != "nan") &
               ( df["Average Cost for two"] != "nan") &
               ( df["Currency"] != "nan") &
               ( df["Has Table booking"] != "nan") &
               ( df["Has Online delivery"] != "nan") &
               ( df["Is delivering now"] != "nan") &
               ( df["Switch to order menu"] != "nan") &
               ( df["Price range"] != "nan") &
               ( df["Aggregate rating"] != "nan") &
               ( df["Rating color"] != "nan") &
               ( df["Rating text"] != "nan") &
               ( df["Votes"] != "nan"))
    df["Cuisines"] = df.loc[:, "Cuisines"].astype(str).apply(lambda x: x.split(",")[0])
    df = df.drop(columns=['Switch to order menu'])
    df = df.drop_duplicates()
    df = df.loc[filtros,:].reset_index(drop=True)
    return df

################################# Funções do projeto

#==============================================INÍCIO DO CÓDIGO==============================================

#carregamento do arquivo
df = pd.read_csv('dataset/zomato.csv')

df1 = clean_code(df)

#inserindo a coluna de nome de países
#df1 = df1.loc[:, ['Country Code']]
df1['Country'] = df1['Country Code'].apply(country_name)
countries = df1['Country'].unique()

#==============================================CRIANDO A SIDEBAR=============================================

image = Image.open('logo.png')

col1, col2 = st.columns(2)

st.sidebar.image(image, width = 100)
st.sidebar.markdown('# Fome Zero')

st.sidebar.markdown('## Filtros')
st.sidebar.markdown("""---""")

country = st.sidebar.multiselect('Escolha os países que deseja visualizar os restaurantes', countries, default = countries[:5])

linhas_selecionadas = df1['Country'].isin(country)
df1 = df1.loc[linhas_selecionadas, :]

st.sidebar.markdown("""---""")

#==============================================FIM DA SIDEBAR================================================


#==============================================INÍCIO DO LAYOUT==============================================

st.markdown('# Visão Cidades')
st.markdown('''---''')

with st.container():
    
    st.markdown('### Top 10 Cidades com mais Restaurantes Cadastrados')
    #definindo colunas
    colunas = ['Restaurant ID', 'Country Code', 'City']
    #agrupando
    df_aux = df1.loc[:, colunas].groupby(['Country Code', 'City']).nunique().reset_index()
    #aplicando funções
    df_aux['País'] = df_aux['Country Code'].apply(country_name)
    #excluindo colunas
    df_aux = df_aux.drop(['Country Code'], axis = 1)
    #ordenando
    df_aux = df_aux.sort_values('Restaurant ID', ascending = False).reset_index(drop=True)
    #filtrando um top
    df_aux = df_aux.loc[df_aux.index < 10, :].reset_index(drop=True)
    #renomeando
    df_aux = df_aux.rename(columns= {'City' : 'Cidade', 'Restaurant ID' : 'Quantidade de restaurantes'})
    #plotando
    graphic = px.bar(df_aux, x='Cidade', y='Quantidade de restaurantes', color='País', text_auto='Quantidade de restaurantes')
    st.plotly_chart(graphic, use_container_width=True)
    
with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('### Top 10 Cidades com Restaurantes com Média de Avaliação Acima de 4.0')
        #colunas e filtros
        colunas = ['Restaurant ID', 'City', 'Country Code']
        filtro = (df1['Aggregate rating'] > 4) & (df1['Votes'] > 0)
        #agrupando
        df_aux = df1.loc[filtro, colunas].groupby(['Country Code', 'City']).nunique().reset_index()
        #aplicando filtros
        df_aux['País'] = df_aux['Country Code'].apply(country_name)
        #ordenando
        df_aux = df_aux.sort_values('Restaurant ID', ascending = False).reset_index(drop=True)
        #filtrando um top
        df_aux = df_aux.loc[df_aux.index < 7, :].reset_index(drop=True)
        #renomeando
        df_aux = df_aux.rename(columns = { 'City' : 'Cidade', 'Restaurant ID' : 'Quantidade de restaurantes'})
        graphic = px.bar(df_aux, x='Cidade', y='Quantidade de restaurantes', color='País', text='Quantidade de restaurantes')
        st.plotly_chart(graphic, use_container_width=True)
        
    with col2:
        st.markdown('### Top 7 Cidades com Restaurantes com Média de Avaliação Abaixo de 2.0')
        #colunas e filtros
        colunas = ['Restaurant ID', 'City', 'Country Code', 'Aggregate rating']
        filtro = (df1['Aggregate rating'] < 2.5) & (df1['Votes'] > 0)
        #agrupando
        df_aux = df1.loc[filtro, colunas].groupby(['Country Code', 'City']).nunique().reset_index()
        #aplicando funções
        df_aux['País'] = df_aux['Country Code'].apply(country_name)
        #ordenando
        df_aux = df_aux.sort_values('Restaurant ID', ascending = False).reset_index(drop=True)
        #criando um top
        df_aux = df_aux.loc[df_aux.index < 7, :].reset_index(drop=True)
        #excluíndo colunas desnecessárias
        df_aux = df_aux.drop(['Country Code'], axis = 1)
        #renomeando
        df_aux = df_aux.rename( columns = { 'City' : 'Cidade', 'Restaurant ID' : 'Quantidade de retaurantes'})
        #plotando
        graphic = px.bar(df_aux, x='Cidade', y='Quantidade de retaurantes', color='País', text='Quantidade de retaurantes')
        st.plotly_chart(graphic, use_container_width=True)
        
with st.container():
    st.markdown('### Top 7 Cidades mais Restaurantes com Tipos Culinários Distintos')
    #Definindo colunas
    colunas = ['Cuisines', 'City', 'Country Code']
    #agrupando a quantidade distinta de culinárias por cidade
    df_aux = df1.loc[:, colunas].groupby(['Country Code','City']).nunique().reset_index()
    #aplicando funções: nomeando países e nomeando cores
    df_aux['País'] = df_aux['Country Code'].apply(country_name)
    #ordenando o dataframe em ordem decrescente
    df_aux = df_aux.sort_values('Cuisines', ascending = False).reset_index(drop=True)
    #filtrando as 10 primeiras linhas do dataframe
    df_aux = df_aux.loc[0:9, :]
    #excluído colunas desnecessárias
    df_aux = df_aux.drop(['Country Code'], axis = 1)
    #renomeando colunas
    df_aux = df_aux.rename(columns = {'City' : 'Cidade', 'Cuisines' : 'Quantidade de culinárias'})
    #criando e exibindo o gráfico
    graphic = px.bar(df_aux, x='Cidade', y='Quantidade de culinárias', color='País' ,text_auto='Quantidade de culinárias')
    st.plotly_chart(graphic, use_container_width=True)