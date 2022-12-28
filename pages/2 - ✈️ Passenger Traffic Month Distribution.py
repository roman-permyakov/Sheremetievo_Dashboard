import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import seaborn as sns
import altair as alt
#CWD = f'/content/drive/MyDrive/Sherem_streamlit/'
#input_path = f'{CWD}input/'

# Загрузить данные с числом пассажиров в мае-июне
count_all = pd.read_csv('./input/count_all.csv')
count_all['Date_time'] = pd.to_datetime(count_all.Date_time)
count_all ['Month'] = np.where (count_all['Date_time']<'2022-06-01', 'May', 'June')

# Выделить срезы по месяцам
count_may = count_all[count_all['Date_time']<'2022-06-1']
count_june = count_all[(count_all['Date_time']<'2022-07-1')&(count_all['Date_time']>='2022-06-1')]

# Авиакомпании
count_all_airlines_edited = count_all.groupby(['Airline_Name', 'Month'], as_index=False).agg({'count': 'sum'}).sort_values(by =['count'], ascending = False)
count_all_airlines = count_all.groupby('Airline_Name', as_index=False).agg({'count': 'sum'}).sort_values(by =['count'], ascending = False)
count_all_airlines['perc']= count_all_airlines['count']/count_all_airlines['count'].sum()
count_all_airlines['count'] = count_all_airlines['count'].map('{:,.0f}'.format)
count_all_airlines['perc'] = count_all_airlines['perc'].map('{:.2%}'.format)
# Посмотреть соотношение пассажиров разных авиакомпаний в мае
count_may_airlines = count_may.groupby('Airline_Name', as_index=False).agg({'count': 'sum'}).sort_values(by =['count'], ascending = False)
count_may_airlines['perc']= count_may_airlines['count']/count_may_airlines['count'].sum()
count_may_airlines['count'] = count_may_airlines['count'].map('{:,.0f}'.format)
count_may_airlines['perc'] = count_may_airlines['perc'].map('{:.2%}'.format)
# Посмотреть соотношение пассажиров разных авиакомпаний в июне
count_june_airlines = count_june.groupby('Airline_Name', as_index=False).agg({'count': 'sum'}).sort_values(by =['count'], ascending = False)
count_june_airlines['perc']= count_june_airlines['count']/count_june_airlines['count'].sum()
count_june_airlines['count'] = count_june_airlines['count'].map('{:,.0f}'.format)
count_june_airlines['perc'] = count_june_airlines['perc'].map('{:.2%}'.format)

# Страны
count_all_country_edited = count_all.groupby(['COUNTRY', 'Month'], as_index=False).agg({'count': 'sum'}).sort_values(by =['count'], ascending = False)
count_all_country = count_all.groupby('COUNTRY', as_index=False).agg({'count': 'sum'}).sort_values(by =['count'], ascending = False)
count_all_country['perc']= count_all_country['count']/count_all_country['count'].sum()
count_all_country['count'] = count_all_country['count'].map('{:,.0f}'.format)
count_all_country['perc'] = count_all_country['perc'].map('{:.2%}'.format)
# Посмотреть cоотношение пассажиров с разной страной назначения в мае
count_may_country = count_may.groupby('COUNTRY', as_index=False).agg({'count': 'sum'}).sort_values(by =['count'], ascending = False)
count_may_country['perc']= count_may_country['count']/count_may_country['count'].sum()
count_may_country['count'] = count_may_country['count'].map('{:,.0f}'.format)
count_may_country['perc'] = count_may_country['perc'].map('{:.2%}'.format)
# Посмотреть cоотношение пассажиров с разной страной назначения в июне
count_june_country = count_june.groupby('COUNTRY', as_index=False).agg({'count': 'sum'}).sort_values(by =['count'], ascending = False)
count_june_country['perc']= count_june_country['count']/count_june_country['count'].sum()
count_june_country['count'] = count_june_country['count'].map('{:,.0f}'.format)
count_june_country['perc'] = count_june_country['perc'].map('{:.2%}'.format)

# Посмотреть соотношение пассажиров с разным городом назначения
count_all_towns_edited = count_all.groupby(['TOWN', 'Month'], as_index=False).agg({'count': 'sum'}).sort_values(by =['count'], ascending = False)
count_all_towns = count_all.groupby('TOWN', as_index=False).agg({'count': 'sum'}).sort_values(by =['count'], ascending = False)
count_all_towns['perc']= count_all_towns['count']/count_all_towns['count'].sum()
count_all_towns['count'] = count_all_towns['count'].map('{:,.0f}'.format)
count_all_towns['perc'] = count_all_towns['perc'].map('{:.2%}'.format)
# Посмотреть cоотношение пассажиров с разным городом назначения в мае
count_may_towns = count_may.groupby('TOWN', as_index=False).agg({'count': 'sum'}).sort_values(by =['count'], ascending = False)
count_may_towns['perc']= count_may_towns['count']/count_may_towns['count'].sum()
count_may_towns['count'] = count_may_towns['count'].map('{:,.0f}'.format)
count_may_towns['perc'] = count_may_towns['perc'].map('{:.2%}'.format)
# Посмотреть cоотношение пассажиров с разным городом назначения в июне
count_june_towns = count_june.groupby('TOWN', as_index=False).agg({'count': 'sum'}).sort_values(by =['count'], ascending = False)
count_june_towns['perc']= count_june_towns['count']/count_june_towns['count'].sum()
count_june_towns['count'] = count_june_towns['count'].map('{:,.0f}'.format)
count_june_towns['perc'] = count_june_towns['perc'].map('{:.2%}'.format)

import streamlit as st

st.set_page_config(page_title='Forecasting the Revenue of Sheremetievo Airport Retail Outlets',
page_icon='https://alllogos.ru/images/logotip-sheremetevo.png', layout="wide")
#st.sidebar.image('https://pro-tile.ru/upload/resize_cache/iblock/95a/0_80_2/95ad2da1d04ff10c34faa68faa5aebe8.png', width=300)


# Sidebar Configuration
#add_logo("https://a-plex.ru/images/cms/thumbs/a4ffe087c89cb1feaf56d5f8a966f9bebe6ae94b/sheremetievologo_auto_141_png__85.png")

#st.sidebar.markdown('# Predicting Revenues of Sheremetievo Airport Retail Points')

st.sidebar.markdown('''<h2 style="text-align: left;"><img src="https://alllogos.ru/images/logotip-sheremetevo.png" width="25"/>
Sheremetievo Airport. Forecasting the Revenue of Retail Outlets</h2>''',
unsafe_allow_html=True)

st.sidebar.markdown('Sheremetievo is the second largest airport in Europe in terms of passenger traffic per year.')
st.sidebar.markdown('This App is designed to display revenue forecasts of retail outlets in June 2022 based on real revenue in May 2022 and passenger traffic-related features.')

st.sidebar.markdown('''Roman Permyakov ©
    <a href="https://github.com/roman-permyakov">
        <img src="https://www.seonews.ru/upload/resize_cache/iblock/a5b/120_120_1/a5bca6110d2c6c8f8e0ab44675750a7c.jpg" width="35" />
    </a>''',
    unsafe_allow_html=True
)

# New
#st.markdown('# **Passenger Traffic Month Distribution ✈️**')
st.markdown("<h1>Passenger Traffic Month Distribution ✈️</h1>", unsafe_allow_html=True)
st.markdown('##### **Real Data. May-June 2022**')
st.markdown("\n\n")

# Selectbox
option = st.selectbox('Select Parameter of Passengers Distribution ✈️', ['Airlines', 'Destination Country', 'Destination Town'])

if option == "Airlines":
  col1, col2, col3 = st.columns(3)
  with col1:
    st.write ('Output Tables 📝: May, 2022')
    st.dataframe(data=count_may_airlines, width=None, height=420, use_container_width=True)
    
  with col2:
    st.write ('June, 2022')
    st.dataframe(data=count_june_airlines, width=None, height=420, use_container_width=True)

  with col3:
    st.write ('Total, 2022')
    st.dataframe(data=count_all_airlines, width=None, height=420, use_container_width=True)

  st.write ('Output Bar Chart 📊')
  domain = ['May', 'June']
  range_ = ['#c748b6', '#48b6c7']

   
  #click = alt.selection_multi(encodings=['color'])
  c = alt.Chart(count_all_airlines_edited).mark_bar().encode(
    x= alt.X ('sum(count)', stack='zero', title = 'Passengers'),
    y= alt.Y ('Airline_Name', sort=['-x', 'count']),
    color=alt.Color('Month:O', sort=['x', 'Month'], scale=alt.Scale(domain=domain, range=range_)),
    #color=alt.condition(click, color, alt.value('black')),
    tooltip = ['Airline_Name', alt.Tooltip('sum(count):Q',format=',.0f', title = 'Passengers'), 'Month']).properties()#.add_selection(click)
  st.altair_chart (c, use_container_width=True)

if option == "Destination Country":
  col1, col2, col3 = st.columns(3)
  with col1:
    st.write ('Output Tables 📝: May, 2022')
    st.dataframe(data=count_may_country, width=120, height=420, use_container_width=True)
    
  with col2:
    st.write ('June, 2022')
    st.dataframe(data=count_june_country, width=120, height=420, use_container_width=True)

  with col3:
    st.write ('Total, 2022')
    st.dataframe(data=count_all_country, width=120, height=420, use_container_width=True)

  st.write ('Output Bar Chart 📊')
  domain = ['May', 'June']
  range_ = ['#c748b6', '#48b6c7']
   
  #click = alt.selection_multi(encodings=['color'])
  c = alt.Chart(count_all_country_edited).mark_bar().encode(
    x= alt.X ('sum(count)', stack='zero', title = 'Passengers'),
    y= alt.Y ('COUNTRY', sort=['-x', 'count']),
    color=alt.Color('Month:O', sort=['x', 'Month'], scale=alt.Scale(domain=domain, range=range_)),  
    #color=alt.condition(click, color, alt.value('lightgray')),
    tooltip = ['COUNTRY', alt.Tooltip('sum(count):Q',format=',.0f', title = 'Passengers'), 'Month']).properties()#.add_selection(click)
  st.altair_chart (c, use_container_width=True)

if option == "Destination Town":
  col1, col2, col3 = st.columns(3)
  with col1:
    st.write ('Output Tables 📝: May, 2022')
    st.dataframe(data=count_may_towns, width=120, height=420, use_container_width=False)
    
  with col2:
    st.write ('June, 2022')
    st.dataframe(data=count_june_towns, width=120, height=420, use_container_width=False)

  with col3:
    st.write ('Total, 2022')
    st.dataframe(data=count_all_towns, width=120, height=420, use_container_width=False)

  st.write ('Output Bar Chart 📊')  

  domain = ['May', 'June']
  range_ = ['#c748b6', '#48b6c7']
  

  #click = alt.selection_multi(encodings=['color'])
  c = alt.Chart(count_all_towns_edited).mark_bar().encode(
    x= alt.X ('sum(count)', stack='zero', title = 'Passengers'),
    y= alt.Y ('TOWN', sort=['-x', 'count']),
    color=alt.Color('Month:O', sort=['x', 'Month'], scale=alt.Scale(domain=domain, range=range_)),  
    #color=alt.condition(click, color, alt.value('lightgray')),
    tooltip = ['TOWN', alt.Tooltip('sum(count):Q',format=',.0f', title = 'Passengers'), 'Month']).properties()#.add_selection(click)
  st.altair_chart (c, use_container_width=True)

