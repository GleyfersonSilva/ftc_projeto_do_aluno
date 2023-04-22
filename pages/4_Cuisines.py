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
    page_title="Culinárias",
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

def avaliation_restaurant(df1, rank_asc, indice):
    '''
    Esta função tem o objetivo de trazer as informações do melhor ou pior restaurante do top 5 melhores ou piores restaurantes
    df: dataframe a ser analisado
    rank_asc: a ordenação da análise
        - False: irá analisar os melhores restaurantes
        - True: irá analisar os piores restaurantes
    indice: indica qual dos top 5 restaurantes você deseja exibir
        - exemplo: o top restaurantes vai de 1 a 5, porém, como temos o indice iniciando em 0, precisamos 
        utilizar os valores de 0 a 4 para indicar esses restaurantes, sendo 0 o primeiro restaurante e 4 o último restaurante.
    '''
    # Obter os 5 tipos de culinária com a maior média de avaliação
    # Filtros e colunas
    colunas = ['Aggregate rating', 'Cuisines']
    filtros = (df1['Votes'] > 0) & (df1['Cuisines'] != 'Others') & (df1['Cuisines'] != 'nan')

    df_aux = df1.loc[filtros, colunas].groupby(['Cuisines']).mean().reset_index()
    df_aux = df_aux.sort_values('Aggregate rating', ascending = rank_asc).reset_index(drop=True)
    df_aux = df_aux.loc[:4, ['Cuisines']]
    culinarias = list(df_aux['Cuisines'])

    #Filtrando somente as restaurantes que servem as top 5 culinárias
    df_aux = df1.loc[(df1['Cuisines'].isin(culinarias)), :]

    #Filtrando apenas o restaurante com a maior média, da culinária top 1
    filtros = (df_aux['Cuisines'] == culinarias[indice])
    colunas = ['Country Code', 'City', 'Average Cost for two', 'Currency', 'Restaurant Name', 'Aggregate rating', 'Cuisines']
    df_aux = df_aux.loc[filtros, colunas]
    df_aux = df_aux.sort_values('Aggregate rating', ascending = rank_asc).reset_index(drop=True)
    df_aux = df_aux.loc[:0, :]
    df_aux['País'] = df_aux['Country Code'].apply(country_name)
    df_aux = df_aux.rename( columns = {'Average Cost for two' : 'Média de um prato para dois', 'Currency' : 'Moeda', 'Restaurant Name' : 'Restaurante', 'City' : 'Cidade', 'Cuisines' : 'Culinária', 'Aggregate rating' : 'Avaliação'})
    df_aux = df_aux.drop(['Country Code'], axis=1)
    return df_aux

#Top melhores e piores restaurantes
def rank_restaurant(df1, rank_asc, indice):
    '''
        Esta função tem o objetivo de trazer as informações de um rank de 1 a 20 piores ou melhores restaurantes
        df: dataframe a ser analisado
        rank_asc: a ordenação da análise
            - False: irá analisar os melhores restaurantes
            - True: irá analisar os piores restaurantes
        indice: indica qual o top restaurantes você deseja exibir
            - exemplo: a partir de um filtro de valores é definido um número, de 1 a 20, onde deve ser escolhido a quantidade de restaurantes que deve conter este rank
    '''
    filtros = (df1['Votes'] > 0) & (df1['Cuisines'] != 'Others') & (df1['Cuisines'] != 'nan')
    colunas = ['Restaurant ID', 'Restaurant Name', 'Country Code', 'City', 'Cuisines', 'Average Cost for two', 'Aggregate rating', 'Votes']
    df_aux = df1.loc[filtros, colunas].reset_index(drop=True)
    df_aux = df_aux.sort_values('Aggregate rating', ascending = rank_asc).reset_index(drop=True)
    df_aux = df_aux.loc[filtros, :]
    return df_aux

def avaliation_cuisines(df1, rank_asc, indice):
    '''
        Esta função tem o objetivo de trazer um gráfico de barras de um rank de 1 a 20 piores ou melhores culinárias
        df: dataframe a ser analisado
        rank_asc: a ordenação da análise
            - False: irá analisar os melhores restaurantes
            - True: irá analisar os piores restaurantes
        indice: indica qual o top restaurantes você deseja exibir
            - exemplo: a partir de um filtro de valores é definido um número, de 1 a 20, onde deve ser escolhido a quantidade de restaurantes que deve conter este rank
    '''
    colunas = ['Aggregate rating', 'Cuisines']
    filtros = (df1['Votes'] > 0) & (df1['Cuisines'] != 'Others')
    df_aux = df1.loc[filtros, colunas].groupby(['Cuisines']).mean().reset_index()
    df_aux = df_aux.sort_values('Aggregate rating', ascending = rank_asc).reset_index(drop=True)
    df_aux = df_aux.rename(columns = {'Cuisines' : 'Culinária', 'Aggregate rating' : 'Média das avaliações'})
    df_aux = df_aux.loc[:indice, :]

    graph = px.bar(df_aux, x='Culinária', y='Média das avaliações', text_auto='.2f')
    return graph
#==============================================INÍCIO DO CÓDIGO==============================================

#carregamento do arquivo
df = pd.read_csv('dataset/zomato.csv')

df1 = clean_code(df)

#inserindo a coluna de nome de países
#df1 = df1.loc[:, ['Country Code']]
df1['Country'] = df1['Country Code'].apply(country_name)
countries = df1['Country'].unique()
cuisines = df1['Cuisines'].unique()
#==============================================CRIANDO A SIDEBAR=============================================

image = Image.open('logo.png')

col1, col2 = st.columns(2)

st.sidebar.image(image, width = 100)
st.sidebar.markdown('# Fome Zero')
st.sidebar.markdown("""---""")
st.sidebar.markdown('## Filtros')
#Filtro países
country = st.sidebar.multiselect('Escolha os países que deseja visualizar os restaurantes', countries, default = countries[:5])
linhas_selecionadas = df1['Country'].isin(country)
df1 = df1.loc[linhas_selecionadas, :]

#Filtro top países
slider = st.sidebar.slider(
    'Selecione a Quantidade de Restaurantes que Deseja Visualizar',
    value = 5,
    min_value = 1,
    max_value = 20 )


#Filtro Cidades
culinaria = st.sidebar.multiselect('Escolha os tipos de culinária que deseja visualizar', cuisines, default = cuisines)
linhas_selecionadas = df1['Cuisines'].isin(culinaria)
df1 = df1.loc[linhas_selecionadas, :].reset_index(drop=True)

st.sidebar.markdown("""---""")

#==============================================FIM DA SIDEBAR================================================


#==============================================INÍCIO DO LAYOUT==============================================


st.markdown('# Visão Tipos de Culinárias')
st.markdown('''---''')

st.markdown('### Melhores restaurantes dos Principais Tipos Culinários')

with st.container():
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        df_auxiliar = avaliation_restaurant(df1, rank_asc=False, indice= 0)
        titulo  = df_auxiliar.iloc[0,5] + ': ' + df_auxiliar.iloc[0,3]
        valor = df_auxiliar.iloc[0,4].astype(str)  + "/5.0"
        ajuda = 'País: ' + df_auxiliar.iloc[0,6] +'\n\n Cidade: ' +df_auxiliar.iloc[0,0] + '\n\n Média de Prato Para Dois: '  + df_auxiliar.iloc[0,1].astype(str) + df_auxiliar.iloc[0,2]
        st.metric(label=titulo, value = valor, help=ajuda)
        
    with col2:
        df_auxiliar = avaliation_restaurant(df1, rank_asc=False, indice= 1)
        titulo  = df_auxiliar.iloc[0,5] + ': ' + df_auxiliar.iloc[0,3]
        valor = df_auxiliar.iloc[0,4].astype(str)  + "/5.0"
        ajuda = 'País: ' + df_auxiliar.iloc[0,6] +'\n\n Cidade: ' +df_auxiliar.iloc[0,0] + '\n\n Média de Prato Para Dois: '  + df_auxiliar.iloc[0,1].astype(str) + df_auxiliar.iloc[0,2]
        st.metric(label=titulo, value = valor, help=ajuda)
        
    with col3:
        df_auxiliar = avaliation_restaurant(df1, rank_asc=False, indice= 2)
        titulo  = df_auxiliar.iloc[0,5] + ': ' + df_auxiliar.iloc[0,3]
        valor = df_auxiliar.iloc[0,4].astype(str)  + "/5.0"
        ajuda = 'País: ' + df_auxiliar.iloc[0,6] +'\n\n Cidade: ' +df_auxiliar.iloc[0,0] + '\n\n Média de Prato Para Dois: '  + df_auxiliar.iloc[0,1].astype(str) + df_auxiliar.iloc[0,2]
        st.metric(label=titulo, value = valor, help=ajuda)
        
    with col4:
        df_auxiliar = avaliation_restaurant(df1, rank_asc=False, indice= 3)
        titulo  = df_auxiliar.iloc[0,5] + ': ' + df_auxiliar.iloc[0,3]
        valor = df_auxiliar.iloc[0,4].astype(str)  + "/5.0"
        ajuda = 'País: ' + df_auxiliar.iloc[0,6] +'\n\n Cidade: ' +df_auxiliar.iloc[0,0] + '\n\n Média de Prato Para Dois: '  + df_auxiliar.iloc[0,1].astype(str) + df_auxiliar.iloc[0,2]
        st.metric(label=titulo, value = valor, help=ajuda)
        
    with col5:
        df_auxiliar = avaliation_restaurant(df1, rank_asc=False, indice= 4)
        titulo  = df_auxiliar.iloc[0,5] + ': ' + df_auxiliar.iloc[0,3]
        valor = df_auxiliar.iloc[0,4].astype(str)  + "/5.0"
        ajuda = 'País: ' + df_auxiliar.iloc[0,6] +'\n\n Cidade: ' +df_auxiliar.iloc[0,0] + '\n\n Média de Prato Para Dois: '  + df_auxiliar.iloc[0,1].astype(str) + df_auxiliar.iloc[0,2]
        st.metric(label=titulo, value = valor, help=ajuda)

st.markdown('### Piores restaurantes dos Tipos Culinários com menor média de avaliação')

with st.container():
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        df_auxiliar = avaliation_restaurant(df1, rank_asc=True, indice= 0)
        titulo  = df_auxiliar.iloc[0,5] + ': ' + df_auxiliar.iloc[0,3]
        valor = df_auxiliar.iloc[0,4].astype(str)  + "/5.0"
        ajuda = 'País: ' + df_auxiliar.iloc[0,6] +'\n\n Cidade: ' +df_auxiliar.iloc[0,0] + '\n\n Média de Prato Para Dois: '  + df_auxiliar.iloc[0,1].astype(str) + df_auxiliar.iloc[0,2]
        st.metric(label=titulo, value = valor, help=ajuda)
        
    with col2:
        df_auxiliar = avaliation_restaurant(df1, rank_asc=True, indice= 1)
        titulo  = df_auxiliar.iloc[0,5] + ': ' + df_auxiliar.iloc[0,3]
        valor = df_auxiliar.iloc[0,4].astype(str)  + "/5.0"
        ajuda = 'País: ' + df_auxiliar.iloc[0,6] +'\n\n Cidade: ' +df_auxiliar.iloc[0,0] + '\n\n Média de Prato Para Dois: '  + df_auxiliar.iloc[0,1].astype(str) + df_auxiliar.iloc[0,2]
        st.metric(label=titulo, value = valor, help=ajuda)
        
    with col3:
        df_auxiliar = avaliation_restaurant(df1, rank_asc=True, indice= 2)
        titulo  = df_auxiliar.iloc[0,5] + ': ' + df_auxiliar.iloc[0,3]
        valor = df_auxiliar.iloc[0,4].astype(str)  + "/5.0"
        ajuda = 'País: ' + df_auxiliar.iloc[0,6] +'\n\n Cidade: ' +df_auxiliar.iloc[0,0] + '\n\n Média de Prato Para Dois: '  + df_auxiliar.iloc[0,1].astype(str) + df_auxiliar.iloc[0,2]
        st.metric(label=titulo, value = valor, help=ajuda)
        
    with col4:
        df_auxiliar = avaliation_restaurant(df1, rank_asc=True, indice= 3)
        titulo  = df_auxiliar.iloc[0,5] + ': ' + df_auxiliar.iloc[0,3]
        valor = df_auxiliar.iloc[0,4].astype(str)  + "/5.0"
        ajuda = 'País: ' + df_auxiliar.iloc[0,6] +'\n\n Cidade: ' +df_auxiliar.iloc[0,0] + '\n\n Média de Prato Para Dois: '  + df_auxiliar.iloc[0,1].astype(str) + df_auxiliar.iloc[0,2]
        st.metric(label=titulo, value = valor, help=ajuda)
        
    with col5:
        df_auxiliar = avaliation_restaurant(df1, rank_asc=True, indice= 4)
        titulo  = df_auxiliar.iloc[0,5] + ': ' + df_auxiliar.iloc[0,3]
        valor = df_auxiliar.iloc[0,4].astype(str)  + "/5.0"
        ajuda = 'País: ' + df_auxiliar.iloc[0,6] +'\n\n Cidade: ' +df_auxiliar.iloc[0,0] + '\n\n Média de Prato Para Dois: '  + df_auxiliar.iloc[0,1].astype(str) + df_auxiliar.iloc[0,2]
        st.metric(label=titulo, value = valor, help=ajuda)
 
st.markdown('''---''')

with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('### Top ' + str(slider) + ' Melhores Restaurantes')
        dataframe = rank_restaurant(df1, rank_asc=False, indice=slider)
        dataframe = dataframe.loc[dataframe.index <= slider, :]
        dataframe
        
    with col2:
        st.markdown('### Top ' + str(slider) + ' Piores Restaurantes')
        dataframe = rank_restaurant(df1, rank_asc=True, indice=slider)
        dataframe = dataframe.loc[dataframe.index <= slider, :]
        dataframe
        
with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('### Top ' + str(slider) + ' Melhores Tipos de Culinária')
        graphic = avaliation_cuisines(df1, rank_asc=False, indice=slider-1)
        st.plotly_chart(graphic, use_container_width=True)
        
    with col2:
        st.markdown('### Top ' + str(slider) + ' Piores Tipos de Culinária')
        graphic = avaliation_cuisines(df1, rank_asc=True, indice=slider-1)
        st.plotly_chart(graphic, use_container_width=True)
        
