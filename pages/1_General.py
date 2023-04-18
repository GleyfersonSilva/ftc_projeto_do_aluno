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
    page_title="Dados gerais",
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


def unique_values(df1, coluna):
    '''
    Esta função tem o objetivo de trazer a contagem de valores únicos de uma coluna do dataframe
    df - dataframe a ser analisado
    coluna - deve ser passado o nome da coluna que deseja obter a soma da quantidade de valores únicos
    '''
    qtd = df1[coluna].nunique()
    return qtd

#criação do mapa
def restaurant_map(df1):
    lat = list(df1['Latitude'])
    long = list(df1['Longitude'])
    map = folium.Map(zoom_start=5,width='%100', height='%100')
    location=df1[["Latitude","Longitude"]]
    folium.plugins.MarkerCluster(location).add_to(map)
    folium_static(map, width=1540, height=600)
    return map

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

country = st.sidebar.multiselect('Escolha os países que deseja visualizar os restaurantes', countries, default = countries)

linhas_selecionadas = df1['Country'].isin(country)
df1 = df1.loc[linhas_selecionadas, :]

st.sidebar.markdown("""---""")

#==============================================FIM DA SIDEBAR================================================


#==============================================INÍCIO DO LAYOUT==============================================

st.markdown('# Fome Zero!')
st.markdown('## O melhor lugar para encontrar seu mais novo restaurante favorito!')
st.markdown('### Temos as seguintes marcas dentro da nossa plataforma')
st.markdown('''---''')

with st.container():
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        value = unique_values(df1, coluna='Restaurant ID')
        st.metric('Restaurantes cadastrados', value)
    with col2:
        value = unique_values(df1, coluna='Country Code')
        st.metric('Países cadastrados', value)
    with col3:
        value = unique_values(df1, coluna='City')
        st.metric('Cidades cadastradas', value)
    with col4:
        value = unique_values(df1, coluna='Cuisines')
        st.metric('Culinárias cadastradas', value)
    with col5:
        value = df1['Aggregate rating'].sum()
        st.metric('Quantidade de avaliações', value)
with st.container():
    st.markdown('''---''')
    st.markdown('## Distribuição mundial de restaurantes')
    restaurant_map(df1)
    

