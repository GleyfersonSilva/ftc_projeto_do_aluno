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
    page_title="Países",
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

st.markdown('# Visão Países')
st.markdown('''---''')

with st.container():
    st.markdown('### Quantidade de Restaurantes Registrados por País')
    colunas = ['Restaurant ID', 'Country Code']
    df_aux = df1.loc[:, colunas].groupby(['Country Code']).nunique().reset_index()
    df_aux['País'] = df_aux['Country Code'].apply(country_name)
    df_aux = df_aux.rename(columns={'Restaurant ID': 'Qtd Restaurantes'})
    df_aux = df_aux.drop(['Country Code'], axis = 1)
    df_aux = df_aux.sort_values('Qtd Restaurantes', ascending = False)
    graphic = px.bar(df_aux, x='País', y='Qtd Restaurantes', text_auto = True)
    st.plotly_chart(graphic, use_container_width= True)
    
with st.container():
    st.markdown('### Quantidade de Cidades Registradas por País')
    colunas = ['City', 'Country Code']
    df_aux = df1.loc[:, colunas].groupby(['Country Code']).nunique().reset_index()
    df_aux['País'] = df_aux['Country Code'].apply(country_name)
    df_aux = df_aux.rename(columns={'City' : 'Qtd Cidades'})
    df_aux = df_aux.drop(['Country Code'], axis = 1)
    df_aux = df_aux.sort_values('Qtd Cidades', ascending = False)
    graphic = px.bar(df_aux, x='País', y='Qtd Cidades', text_auto = True)
    st.plotly_chart(graphic, use_container_width = True)
    
with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('### Média de Avaliações por País')
        colunas = ['Votes', 'Country Code']
        df_aux = df1.loc[:, colunas].groupby(['Country Code']).mean().reset_index()
        df_aux['País'] = df_aux['Country Code'].apply(country_name)
        df_aux = df_aux.drop(['Country Code'], axis=1)
        df_aux = df_aux.sort_values('Votes', ascending = False)
        df_aux = df_aux.rename(columns={'Votes' : 'Quantidade de avaliações'})
        graphic = px.bar(df_aux, x='País', y='Quantidade de avaliações', text_auto='.2f')
        st.plotly_chart(graphic, use_container_width = True)
        
    with col2:
        st.markdown('### Média de Preço de um Prato para Duas Pessoas por País')
        colunas = ['Average Cost for two', 'Country Code']
        df_aux = df1.loc[:, colunas].groupby(['Country Code']).mean().reset_index()
        df_aux['País'] = df_aux['Country Code'].apply(country_name)
        df_aux = df_aux.drop(['Country Code'], axis = 1)
        df_aux = df_aux.sort_values('Average Cost for two', ascending = False)
        df_aux = df_aux.rename(columns = {'Average Cost for two' : 'Preço médio de um prato para duas pessoas'})
        graphic = px.bar(df_aux, x='País', y='Preço médio de um prato para duas pessoas', text_auto='.2f')
        st.plotly_chart(graphic, use_container_width=True)
        



