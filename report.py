"""
Created on Wen Jan 17 2022
@author: Carlos Silva
"""
from ctypes import alignment
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title='Seazone - Desafio',  layout='wide', page_icon='./img/seazone-icon.png')

@st.cache( allow_output_mutation=True )
def data_collect( path) :
    data =  pd.read_csv( path, index_col=0 )

    return data

def data_cleaning( details_raw, priceav_raw ):
    # Remove features desnecessárias para análise
    details_df = details_raw.drop(columns=['ad_name'])
    priceav_df = priceav_raw.drop(columns=['Unnamed: 0.1'])

    # Droping data que possui quantidade insignificante de missing values
    details_df = details_df.dropna(subset=['number_of_bathrooms', 'number_of_reviews','number_of_bedrooms'])

    # Completando missing values que são muito importantes para serem eliminados, preenchendo-os com a mediana entre eles
    details_df = details_df.fillna(details_df['star_rating'].median())

    # Alterando Supehost 0 = Não; 1 = Sim
    details_df['is_superhost'].replace({False: 0, True: 1}, inplace=True)

    # Ignorando o valor do tempo presente em 'booked_on'
    priceav_df = priceav_df
    priceav_df['booked_on'] = priceav_df['booked_on'].apply(lambda x: x.split(' ')[0])

    return details_df, priceav_df

def header():
    t1, t2 = st.columns((1, 3)) 

    t1.image('img/seazone-icon.png', width = 120)
    t2.title("Seazone - Desafio Prático")
    t2.markdown( "O desafio consiste em analisar os dados de ocupação e preço de anúncios no Airbnb, a fim de responder uma série de perguntas." )
    t2.markdown( "Com o proposito de solucionar o desafio proposto pela [Seazone](https://seazone.com.br/) para o processo seletivo da vaga de Analista de Dados Jr. " )
    t2.markdown( "**tel:** (92) 99157-2061 **| github:** [carlosgsilva](https://github.com/carlosgsilva) **| email:** mailto:carlosgsilva.dev@gmail.com" )
    return None

def data_overview( data_details, data_priceav ):

    cw1, cw2 = st.columns((2.5, 1.7))

    data_details_df = data_details.copy()
    data_priceav_df = data_priceav.copy()
    
    # Renomeando as colunas
    data_details_df.columns = ['Listing', 'Bairro', 'Quartos', 'Banheiros', 'Pontuação', 'Superhost',  'Avaliações']
    data_priceav_df.columns = ['Listing', 'Reservado em', 'Data', 'Preço',  'Ocupado']

    # Características de cada anúncios
    fig = go.Figure(
            data = [go.Table (columnorder = [0,1,2,3,4,5,6,], columnwidth = [10, 15, 10, 10, 10, 10, 10],
                header = dict(
                 values = list(data_details_df.columns),
                 font=dict(size=12, color = 'white'),
                 fill_color = '#264653',
                 line_color = 'rgba(255,255,255,0.2)',
                 align = ['left','center'],
                 #text wrapping
                 height=20
                 )
              , cells = dict(
                  values = [data_details_df[K].tolist() for K in data_details_df.columns], 
                  font=dict(size=12),
                  align = ['left','center'],
                  line_color = 'rgba(255,255,255,0.2)',
                  height=20))])
    
    fig.update_layout(title_text="Características de cada anúncio",title_font_color = '#264653',title_x=0,margin= dict(l=0,r=10,b=10,t=30), height=480)  
    cw1.plotly_chart(fig, use_container_width=True)  
    
    # Dados de ocupação e preço de anúncios    
    fig = go.Figure(
            data = [go.Table (columnorder = [0,1, 2, 3, 4], columnwidth = [10, 15, 10, 10, 10],
                header = dict(
                 values = list(data_priceav_df.columns),
                 font=dict(size=12, color = 'white'),
                 fill_color = '#264653',
                 align = 'left',
                 height=20
                 )
              , cells = dict(
                  values = [data_priceav_df[K].tolist() for K in data_priceav_df.columns], 
                  font=dict(size=12),
                  align = 'left',
                  fill_color='#F0F2F6',
                  height=20))]) 
        
    fig.update_layout(title_text="Dados de ocupação e preço de anúncios",title_font_color = '#264653',title_x=0,margin= dict(l=0,r=10,b=10,t=30), height=480)
    cw2.plotly_chart(fig, use_container_width=True)

    return None

def listing_by_suburb( data_details ):

    details_df = data_details.copy()

    with st.expander("Bairros em ordem crescente de número de listings"):
        cw1, cw2 = st.columns( ( 3, 2 ) )

        # Gráfico de listagem em ordem crescente de número de listing
        details_df = details_df.groupby('suburb', as_index=False).airbnb_listing_id.count()
        details_df.sort_values(['airbnb_listing_id'], inplace=True)

        colors = ['lightslategray',] * 5
        colors[-1] = 'crimson'

        fig = px.bar(details_df, x = 'suburb', y='airbnb_listing_id', template='plotly_white')

        fig.update_traces( marker_color=colors, text=details_df.airbnb_listing_id )
        fig.update_layout( title_text="Bairros x Listings", 
                                        title_x=0,margin= dict(l=30,r=10,b=10,t=30), 
                                        yaxis_title='Listings', xaxis_title='Bairros', 
                                        hoverlabel=dict(bgcolor="black",
                                        font_size=13, 
                                        font_family="Lato, sans-serif") )                                                                
        fig.update_yaxes( showticklabels=False )
        fig.add_annotation( dict(x=0.3, y=0.7, ax=0, ay=0,
                    xref = "paper", yref = "paper",
                    text= 'O bairro <b>Ingleses</b> possui o maior número de listings <br> Tendo mais que o dobro de listagens <br> que o bairro <b>Cansvieira</b> que é o segundo no rank.') )
        cw1.plotly_chart( fig, use_container_width=False, align='center' ) 

        # Overview dos dados
        details_df.columns = ['Bairro', 'Quantidade de Listagem']
        fig = go.Figure(
            data = [go.Table (columnorder = [0,1], columnwidth = [15, 15],
                header = dict(
                 values = list(details_df.columns),
                 font=dict(size=12, color = 'white'),
                 fill_color = '#264653',
                 align = 'left',
                 height=20
                 )
              , cells = dict(
                  values = [details_df[K].tolist() for K in details_df.columns], 
                  font=dict(size=12),
                  align = 'left',
                  fill_color='#F0F2F6',
                  height=20))]) 
        
        fig.update_layout(title_text="Quantidade de listagem por bairro",title_font_color = '#264653',title_x=0,margin= dict(l=0,r=10,b=10,t=30), height=480)
        cw2.plotly_chart(fig, use_container_width=True)

    return None

def average_revenues_by_listings( data_details, data_priceav ):
    priceav_df = data_priceav.copy()
    details_df = data_details.copy()

    with st.expander("Bairros em ordem crescente de faturamento médio dos listings"):
        cw1, cw2 = st.columns( ( 3, 2 ) )

        # Combina os datasets
        df = pd.merge(details_df, priceav_df, how='inner')

        # Calcula a média de faturamento dos anúncios por bairro
        df = df.groupby('suburb', as_index=False).price_string.mean().round(2)
        df.sort_values(['price_string'], inplace=True)

        colors = ['lightslategray',] * 5
        colors[-1] = 'crimson'

        fig = px.bar(df, x = 'suburb', y='price_string', template='plotly_white')

        fig.update_traces( marker_color=colors, text=df.price_string, texttemplate="R%{y:$.2f}")
        fig.update_layout( title_text="Bairros x Faturamento", 
                                        title_x=0,margin= dict(l=30,r=10,b=10,t=30), 
                                        yaxis_title='Listings', xaxis_title='Bairros', 
                                        hoverlabel=dict(bgcolor="black",
                                        font_size=13, 
                                        font_family="Lato, sans-serif") )                                                                
        fig.update_yaxes( showticklabels=False )

        cw1.plotly_chart( fig, use_container_width=True ) 

        # Overview dos dados
        df.columns = ['Bairro', 'Quantidade de Listagem (R$)']
        fig = go.Figure(
            data = [go.Table (columnorder = [0,1], columnwidth = [15, 15],
                header = dict(
                 values = list(df.columns),
                 font=dict(size=12, color = 'white'),
                 fill_color = '#264653',
                 align = 'left',
                 height=20
                 )
              , cells = dict(
                  values = [df[K].tolist() for K in df.columns], 
                  font=dict(size=12),
                  align = 'left',
                  fill_color='#F0F2F6',
                  height=20))]) 
        
        fig.update_layout(title_text="Faturamento médio dos listings por bairro",title_font_color = '#264653',title_x=0,margin= dict(l=0,r=10,b=10,t=30), height=480)
        cw2.plotly_chart(fig, use_container_width=True)

    return None

if __name__ == '__main__':
    details_raw = data_collect( './data/desafio_details.csv' )
    priceav_raw = data_collect( './data/desafio_priceav.csv' )

    df_details, df_priceav = data_cleaning( details_raw, priceav_raw )

    header()

    data_overview( df_details, df_priceav  )

    listing_by_suburb( df_details )

    average_revenues_by_listings( df_details, df_priceav )

    