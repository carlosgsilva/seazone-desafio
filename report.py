"""
Created on Wen Jan 17 2022
@author: Carlos Silva
"""
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title='Seazone - Desafio',  layout='wide', page_icon='./img/seazone-icon.png')

@st.cache( allow_output_mutation=True )
def data_collect( path) :
    data =  pd.read_csv( path, index_col=0 )

    return data

def data_cleaning( details_raw, priceav_raw ):
    # Remove colunas desnecessárias para análise
    details_df = details_raw.drop(columns=['ad_name'])
    priceav_df = priceav_raw.drop(columns=['Unnamed: 0.1'])

    # Eliminando dados que possuem missing values
    details_df = details_df.dropna(subset=['number_of_bathrooms', 'number_of_reviews','number_of_bedrooms'])

    # Preenchendo os dados que faltam das avaliações com a mediana
    details_df = details_df.fillna(details_df['star_rating'].median())

    # Alterando Supehost 0 = Não; 1 = Sim
    details_df['is_superhost'].replace({False: 0, True: 1}, inplace=True)   

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

    # Características de cada anúncios (Tabela)
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
    
    fig.update_layout( title_text="Características de cada anúncio",title_font_color = '#264653',title_x=0,margin= dict(l=0,r=10,b=10,t=30), height=480)  
    cw1.plotly_chart( fig, use_container_width=True )  
    
    # Dados de ocupação e preço de anúncios  (Tabela)
    fig = go.Figure(
            data = [go.Table ( columnorder = [0,1, 2, 3, 4], columnwidth = [10, 15, 10, 10, 10],
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
                  height=20))] ) 
        
    fig.update_layout( title_text="Dados de ocupação e preço de anúncios",title_font_color = '#264653',title_x=0,margin= dict(l=0,r=10,b=10,t=30), height=480)
    cw2.plotly_chart( fig, use_container_width=True )

    return None

def listing_by_suburb( data_details ):

    details_df = data_details.copy()

    with st.expander("Bairros em ordem crescente de número de listings"):
        cw1, cw2 = st.columns( ( 3, 2 ) )

        # Gráfico de listagem em ordem crescente de número de listing (Gráfico de Barras)
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
        cw1.plotly_chart( fig, use_container_width=False ) 

        # Overview dos dados (Tabela)
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

        # Calcula a média de faturamento dos anúncios por bairro (Gráfico de barras)
        df = df.groupby('suburb', as_index=False).price_string.mean().round(2)
        df.sort_values(['price_string'], inplace=True)

        colors = ['lightslategray',] * 5
        colors[-1] = 'crimson'

        fig = px.bar(df, x = 'suburb', y='price_string', template='plotly_white')

        fig.update_traces( marker_color=colors, text=df.price_string, texttemplate="R%{y:$.2f}")
        fig.update_layout( title_text="Bairros x Faturamento", 
                                        title_x=0,margin= dict(l=30,r=10,b=10,t=30), 
                                        yaxis_title='Faturamento Médio', xaxis_title='Bairros', 
                                        hoverlabel=dict(bgcolor="black",
                                        font_size=13, 
                                        font_family="Lato, sans-serif") )                                                                
        fig.update_yaxes( showticklabels=False )

        cw1.plotly_chart( fig, use_container_width=True ) 

        # Overview dos dados (Tabela)
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
        
        fig.update_layout(title_text="Faturamento médio dos listings por bairro",
                                        title_font_color = '#264653',
                                        title_x=0, 
                                        margin= dict(l=0,r=10,b=10,t=30),
                                        height=480)
        cw2.plotly_chart(fig, use_container_width=True)

    return None

def correlation( data_details, data_priceav ):

    details_df = data_details.copy()
    priceav_df = data_priceav.copy()

    with st.expander("Existe correlação entre as características de um anúncio e seu faturamento?"):
        cw1, cw2 = st.columns( ( 2, 2 ) )

        # Juntando os DataFrame
        data_df = details_df.merge(priceav_df)

        # Filtrando apenas os imovéis que estão/foram ocupados
        data_df = data_df.loc[data_df['booked_on'] != 'blank']

        # Correlação do DataFrame
        df_corr = data_df[['airbnb_listing_id','number_of_bedrooms','number_of_bathrooms','star_rating','is_superhost','price_string','number_of_reviews']].groupby('airbnb_listing_id').sum()
        df_corr.columns = ['Quartos', 'Banheiros', 'Pontuação', 'Superhost', 'Preço',  'Avaliações']

        # Correlação entre as características de um an úncio e seu faturamento (Mapa de Calor)
        fig, ax = plt.subplots( figsize=(7, 5) )
        plt.title('Correlação das características de um anúncio x faturamento', fontsize = 14)
        sns.heatmap(df_corr.corr(), ax=ax, annot=True, vmin=0.7, vmax=1, cmap='Reds', cbar=False, annot_kws={"size": 8} )
        cw1.write( fig, use_container_width=True ) 

        # Qual a correlação (Conclusão)
        conclusion = """
            <p style=font-size:24px> <b>Conclusão</b> </p>  
            
            ---
            <p style=font-size: 20px; text-align: justify>
            O preço de médio das listagem possui uma forte correlação com o <i>número de quartos</i>, <i>banheiros</i> e <i>pontuação</i>.  
            Podemos observar que a pontuação por estrelas ( 1 - 5 ) tem uma mais influencia no faturamento médio que as avaliações,  
            o que pode ser devido o baixo número de avaliações ou que a pontuação é um dos fatores para determinar o preço.
            </p>
        """
        cw2.markdown( conclusion, unsafe_allow_html=True)

    return None

def advance_booking( data_priceav ):
    priceav_df = data_priceav.copy()

    with st.expander( 'Qual a antecedência média das reservas' ):
        cw1, cw2 = st.columns( ( 3, 2 ) )

        # Filtrando apenas os que já foram/estão ocupados 
        priceav_df = priceav_df.get(priceav_df['occupied']==1)

        # Transformando as colunas 'booked_on' e 'date' em datetime
        priceav_df['booked_on'] = pd.to_datetime(priceav_df['booked_on'])
        priceav_df['date'] = pd.to_datetime(priceav_df['date'])

        #  Adiantamento de reservas por dia da semana
        priceav_df['days_to_book'] = (priceav_df['date'] - priceav_df['booked_on']).dt.days

        # Criando novas colunas nome do dia da semana e número do dia da semana
        priceav_df['day_of_booking'] = priceav_df['booked_on'].dt.day_name()
        priceav_df['days'] = priceav_df['booked_on'].dt.weekday

        # Tirando a média da antencipação do agendamento
        mean_price_df = priceav_df.copy()
        mean_price_df = mean_price_df.groupby(['day_of_booking', 'days'], as_index=False ).days_to_book.mean().round(0)
        mean_price_df = mean_price_df.set_index('days').sort_values(by='days', ascending=True )
        
        # Média Reservas antecipadas por dia da semana (Gráfico de linha)
        traco = go.Scatter(
            x = mean_price_df['day_of_booking'], y = mean_price_df['days_to_book'],
            mode='lines+text',
            line=dict(width=0.5, color='lightslategray', dash='solid'),
            fill='tonexty', fillcolor = 'lightslategray',
            text=mean_price_df['days_to_book'],
            textfont=dict(size=14,color='black'),
            textposition=["top right", "top center", "top center", "top center", "top center", "top center", "top left" ],
            opacity=0.8
         )

        layout = go.Layout(title = 'Reservas Antecipadas x Dia da Semana',
                                         title_font_color = 'black',
                                         margin= dict(l=0,r=10,b=10,t=30),
                                         height=480,
                                         xaxis_title='Dias da Seamana', yaxis_title='Média de Antecedência',
                                         template='plotly_white' )

        fig = go.Figure( data=traco, layout=layout)

        cw1.plotly_chart( fig, use_container_width=True )

        # Classificar os dias da semana entre fim de semana e semana
        def status( mean_price_df ):
            if mean_price_df['day_of_booking'] == 'Saturday' or mean_price_df['day_of_booking'] == 'Sunday':
                return 'weekend'
            return 'week' 
        
        mean_price_df['period'] = mean_price_df.apply(status, axis=1)
        
        # Agrupando pelo perido fim de semana ou semana
        mean_price_df = mean_price_df[['period','days_to_book']].groupby(['period']).mean()

        # Porcentagem de agendamentos Semana x Fim de Semana (Gráfico de Rosca)
        fig = px.pie(mean_price_df, values='days_to_book',
                            names=['Semana','Final de Semana'],
                            hole=.5,
                            title='Verificação da antecedencia média durante semana')

        fig.update_traces(textposition='auto',
                                        textinfo='percent',
                                        textfont_size=20,
                                        marker=dict(colors=['crimson', 'lightslategray']))
        fig.update_layout( title_text="Bairros x Faturamento", 
                                        title_x=0,margin= dict(l=30,r=10,b=10,t=30),
                                        hoverlabel=dict(bgcolor="black",
                                        font_size=8, 
                                        font_family="Lato, sans-serif") )   

        cw2.plotly_chart( fig, use_container_width=True )

        # O número de antecedencia é maior ou menor nos fins de semana (Conclusão
        conclusion = """
            <div align="center" width="500px" >
            <p style=font-size:30px> <b>Conclusão</b> </p>  
            
            ---
            <p style=font-size: 25px; text-align: center>
                Como podemos visualizar nos gráficos, com uma antecedencia média de 40 dias (59,7%) é realizado durante a semana e nos fins de semana <b>27 dias</b> (40,3%). <br>
                Os dias de <i>Quarta</i>, <i>Quinta</i> e <i>Sexta</i> são os dias que as reservas são feitas com mais antecendencia, com uma média de <b>47 dias</b>.
            </p>
            </div>
        """
        st.markdown( conclusion, unsafe_allow_html=True )

    return None

def feedback():

    with st.expander( 'Feedback' ):    
        feedback = """
            <div align="center" width="500px" >
            <p style=font-size:30px> <b>Feedback do Desafio</b> </p>  
            
            ---
            <p style=font-size: 25px; text-align: center>
                Um desafio que por mais simple que parece ser, foi bem desafiador, pude por em prática alguns dos conhecimentos que já tinha e aprender a utilizar
                novas ferramentas para melhorar minhas entregas como o streamlit. O desafio em si possui um objetivo bem claro e direto, as dicas ajudaram muito 
                na parte de planejamento e entrega.
                Agradeço a oportunidade de ter tido essa experiência satisfatória, independente do resultado.
            </p>
            </div>
        """
        st.markdown( feedback, unsafe_allow_html=True )

if __name__ == '__main__':
    details_raw = data_collect( './data/desafio_details.csv' )
    priceav_raw = data_collect( './data/desafio_priceav.csv' )

    df_details, df_priceav = data_cleaning( details_raw, priceav_raw )

    header()

    data_overview( df_details, df_priceav  )

    listing_by_suburb( df_details )

    average_revenues_by_listings( df_details, df_priceav )

    correlation( df_details, df_priceav )

    advance_booking( df_priceav )

    feedback()

    