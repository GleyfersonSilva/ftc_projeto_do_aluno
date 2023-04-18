# importando as bibliotecas
import streamlit as st
from PIL import Image
import pandas as pd
import streamlit.components.v1 as components

#Configurando a página
st.set_page_config(
    page_title="Home",
    layout = "wide"
)

#-----------------FUNÇÕES

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

def convert_df(df1):
    return df1.to_csv().encode('utf-8')

#---------------CARREGANDO E LIMPANDO DATASET
df = pd.read_csv('dataset/zomato.csv')
df1 = clean_code(df)

#-------------CONVERTENDO DATASET PARA CSV
csv = convert_df(df1)

#-------------SIDEBAR
image_path = 'logo.png'
image = Image.open( image_path)
st.sidebar.image( image, width = 120)

st.sidebar.markdown('# Fome Zero')
st.sidebar.markdown('## Análise mundial de restaurantes')
st.sidebar.markdown("""---""")
st.sidebar.markdown('### Dados Tratados')
st.sidebar.download_button(label = 'Download', data = csv, file_name='dados_tratados.csv', mime='text/csv')

#-----------INÍCIO DO CÓDGIO

st.write('# Painel de acompanhamento de crescimento de restaurantes')
st.markdown("""---""")

st.markdown(
    """
        ###  Como utilizar esse Painel de Acompanhamento?
        - General:
            - Métricas gerais e distribuição mundial de restaurantes.
        - Countries:
            - Acompanhamento dos indicadores por país.
        - Cities:
            - Acompanhamento dos indicadores por cidade.
        - Cuisines:
            - Acompanhamento dos indicadores por tipo de culinária.
        ### Ask for Help
        - Time data Science no Discord:
            - @gleyferson
    """) 
