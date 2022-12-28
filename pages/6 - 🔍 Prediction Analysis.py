import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import seaborn as sns
import altair as alt
#CWD = f'/content/drive/MyDrive/Sherem_streamlit/'
#input_path = f'{CWD}input/'
#solution_path = f'{CWD}solutions/'

# Загрузить данные о целевой июньской выручке
revenue_june_target = pd.read_excel ('./solutions/revenue_june_clean.xlsx')
revenue_june_target['Date'] = pd.to_datetime(revenue_june_target.Date)
revenue_june_target['Date_time'] = pd.to_datetime(revenue_june_target.Date_time)

# Предсказания ВЫРУЧКИ В ИЮНЕ
revenue_june_predict_all = pd.read_csv('./solutions/solution_all.csv')
revenue_june_predict_all['Date'] = pd.to_datetime(revenue_june_predict_all.Date)
revenue_june_predict_all['Date_time'] = pd.to_datetime(revenue_june_predict_all.Date_time)

revenue_june_predict_aeroflot = pd.read_csv('./solutions/solution_aeroflot.csv')
revenue_june_predict_aeroflot['Date'] = pd.to_datetime(revenue_june_predict_aeroflot.Date)
revenue_june_predict_aeroflot['Date_time'] = pd.to_datetime(revenue_june_predict_aeroflot.Date_time)

revenue_june_predict_pegas = pd.read_csv('./solutions/solution_pegas.csv')
revenue_june_predict_pegas['Date'] = pd.to_datetime(revenue_june_predict_pegas.Date)
revenue_june_predict_pegas['Date_time'] = pd.to_datetime(revenue_june_predict_pegas.Date_time)

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
#st.markdown('# **Analysis of Revenues Prediction Results🔍**')
st.markdown("<h1>Analysis of Revenue Forecast Results🔍</h1>", unsafe_allow_html=True)
st.markdown("\n\n")

# Selectbox
option = st.selectbox('Select Prediction Model ⚙️', ['All Features', 'Aeroflot', 'Pegas Fly'])

if option == "All Features":

  # Selection for a specific time frame.
  df_select = revenue_june_predict_all
  df_target = revenue_june_target

  col1, col2 = st.columns(2)

  with col1:
      start_date = st.date_input('Select Start Date 📅',min_value= datetime.date(2022,6,1),max_value=datetime.date(2022,6,29),value=datetime.date(2022,6,1))

  with col2:    
      end_date = st.date_input('Select End Date 📅',min_value=datetime.date(2022,6,2),max_value=datetime.date(2022,6,30),value=datetime.date(2022,6,30))

  if(start_date != None or end_date != None):
      if(start_date < end_date):
          s1 = datetime.datetime.combine(start_date, datetime.time.min)
          s2 = datetime.datetime.combine(end_date, datetime.time.min)
          df_select = revenue_june_predict_all[(revenue_june_predict_all['Date_time'] >= s1) & (revenue_june_predict_all['Date_time']<= s2)]
          df_target = revenue_june_target[(revenue_june_target['Date_time'] >= s1) & (revenue_june_target['Date_time']<= s2)]
      else:
          st.warning("Invalid Date Range - Re-enter Dates")  
  
  # Graphs and charts for selected date range.
  place_list_day = df_select['Place'].unique()
  place_list_day.sort()
  place_list_day2 = st.multiselect('Select Retail Outlet 🛒', place_list_day, place_list_day)
  if not place_list_day2:
    st.error("Please select at least one retail outlet")
  else: 
    df_select_day2 = df_select[df_select['Place'].isin(place_list_day2)]
    df_target_day2 = df_target[df_target['Place'].isin(place_list_day2)]

    st.write ('Output Line Chart 📈: Target Revenues')

    highlight = alt.selection(type='single', on='mouseover',
                          fields=['Place'], nearest=True, empty="none")

    base = alt.Chart(df_target_day2).encode(
        x= alt.X('Date_time:T', axis = alt.Axis(labelAngle = 290, format = ("%d.%m.%H:%M"))),
        y = alt.Y('Revenue:Q'),
        color=alt.Color('Place:N', scale=alt.Scale(scheme='tableau20'), legend=alt.Legend(
              columns = 2,
              title = 'Retail Outlets'))).properties(height=410)
          
    points = base.mark_circle().encode(
        size = alt.value(0),
        opacity=alt.value(0),
        tooltip=['Place', alt.Tooltip('Revenue:Q',format=',.0f'), 'Date_time']
    ).add_selection(
        highlight
    ).properties(height=410)

    lines = base.mark_line().encode(
        size=alt.condition(~highlight, alt.value(0.5), alt.value(2))
    )
    st.altair_chart(points + lines, use_container_width=True)
    
    st.write ('Output Line Chart 📈: Predicted Revenues', fontSize = 8)
    pts = alt.selection(type="single", encodings=['x'])
    
    highlight = alt.selection(type='single', on='mouseover',
                          fields=['Place'], nearest=True, empty="none")

    base = alt.Chart(df_select_day2).encode(
        x= alt.X('Date_time:T', axis = alt.Axis(labelAngle = 290, format = ("%d.%m.%H:%M"))),
        y = alt.Y('Revenue:Q'),
        color=alt.Color('Place:N', scale=alt.Scale(scheme='tableau20'), legend=alt.Legend(
              columns = 2,
              title = 'Retail Outlets'))).properties(height=410)
          
    points = base.mark_circle().encode(
        size = alt.value(0),
        opacity=alt.value(0),
        tooltip=['Place', alt.Tooltip('Revenue:Q',format=',.0f'), 'Date_time']
    ).add_selection(
        highlight
    ).properties(height=410)

    lines = base.mark_line().encode(
        size=alt.condition(~highlight, alt.value(0.5), alt.value(2))
    )
    st.altair_chart(points + lines, use_container_width=True)

elif option == "Aeroflot":

  # Selection for a specific time frame.
  df_select = revenue_june_predict_aeroflot
  df_target = revenue_june_target

  col1, col2 = st.columns(2)

  with col1:
      start_date = st.date_input('Select Start Date 📅',min_value= datetime.date(2022,6,1),max_value=datetime.date(2022,6,29),value=datetime.date(2022,6,1))

  with col2:    
      end_date = st.date_input('Select End Date 📅',min_value=datetime.date(2022,6,2),max_value=datetime.date(2022,6,30),value=datetime.date(2022,6,30))

  if(start_date != None or end_date != None):
      if(start_date < end_date):
          s1 = datetime.datetime.combine(start_date, datetime.time.min)
          s2 = datetime.datetime.combine(end_date, datetime.time.min)
          df_select = revenue_june_predict_all[(revenue_june_predict_all['Date_time'] >= s1) & (revenue_june_predict_all['Date_time']<= s2)]
          df_target = revenue_june_target[(revenue_june_target['Date_time'] >= s1) & (revenue_june_target['Date_time']<= s2)]
      else:
          st.warning("Invalid Date Range - Re-enter Dates")  
  
  # Graphs and charts for selected date range.
  place_list_day = df_select['Place'].unique()
  place_list_day.sort()
  place_list_day2 = st.multiselect('Select Retail Outlet 🛒', place_list_day, place_list_day)
  if not place_list_day2:
    st.error("Please select at least one retail outlet")
  else: 
    df_select_day2 = df_select[df_select['Place'].isin(place_list_day2)]
    df_target_day2 = df_target[df_target['Place'].isin(place_list_day2)]

    st.write ('Output Line Chart 📈: Target Revenues')

    highlight = alt.selection(type='single', on='mouseover',
                          fields=['Place'], nearest=True, empty="none")

    base = alt.Chart(df_target_day2).encode(
        x= alt.X('Date_time:T', axis = alt.Axis(labelAngle = 290, format = ("%d.%m.%H:%M"))),
        y = alt.Y('Revenue:Q'),
        color=alt.Color('Place:N', scale=alt.Scale(scheme='tableau20'), legend=alt.Legend(
              columns = 2,
              title = 'Retail Outlets'))).properties(height=410)
          
    points = base.mark_circle().encode(
        size = alt.value(0),
        opacity=alt.value(0),
        tooltip=['Place', alt.Tooltip('Revenue:Q',format=',.0f'), 'Date_time']
    ).add_selection(
        highlight
    ).properties(height=410)

    lines = base.mark_line().encode(
        size=alt.condition(~highlight, alt.value(0.5), alt.value(2))
    )
    st.altair_chart(points + lines, use_container_width=True)
    
    st.write ('Output Line Chart 📈: Predicted Revenues', fontSize = 8)
    pts = alt.selection(type="single", encodings=['x'])
    
    highlight = alt.selection(type='single', on='mouseover',
                          fields=['Place'], nearest=True, empty="none")

    base = alt.Chart(df_select_day2).encode(
        x= alt.X('Date_time:T', axis = alt.Axis(labelAngle = 290, format = ("%d.%m.%H:%M"))),
        y = alt.Y('Revenue:Q'),
        color=alt.Color('Place:N', scale=alt.Scale(scheme='tableau20'), legend=alt.Legend(
              columns = 2,
              title = 'Retail Outlets'))).properties(height=410)
          
    points = base.mark_circle().encode(
        size = alt.value(0),
        opacity=alt.value(0),
        tooltip=['Place', alt.Tooltip('Revenue:Q',format=',.0f'), 'Date_time']
    ).add_selection(
        highlight
    ).properties(height=410)

    lines = base.mark_line().encode(
        size=alt.condition(~highlight, alt.value(0.5), alt.value(2))
    )
    st.altair_chart(points + lines, use_container_width=True)

elif option == "Pegas Fly":

  # Selection for a specific time frame.
  df_select = revenue_june_predict_pegas
  df_target = revenue_june_target

  col1, col2 = st.columns(2)

  with col1:
      start_date = st.date_input('Select Start Date 📅',min_value= datetime.date(2022,6,1),max_value=datetime.date(2022,6,29),value=datetime.date(2022,6,1))

  with col2:    
      end_date = st.date_input('Select End Date 📅',min_value=datetime.date(2022,6,2),max_value=datetime.date(2022,6,30),value=datetime.date(2022,6,30))

  if(start_date != None or end_date != None):
      if(start_date < end_date):
          s1 = datetime.datetime.combine(start_date, datetime.time.min)
          s2 = datetime.datetime.combine(end_date, datetime.time.min)
          df_select = revenue_june_predict_all[(revenue_june_predict_all['Date_time'] >= s1) & (revenue_june_predict_all['Date_time']<= s2)]
          df_target = revenue_june_target[(revenue_june_target['Date_time'] >= s1) & (revenue_june_target['Date_time']<= s2)]
      else:
          st.warning("Invalid Date Range - Re-enter Dates")  
  
  # Graphs and charts for selected date range.
  place_list_day = df_select['Place'].unique()
  place_list_day.sort()
  place_list_day2 = st.multiselect('Select Retail Outlet 🛒', place_list_day, place_list_day)
  if not place_list_day2:
    st.error("Please select at least one retail outlet")
  else: 
    df_select_day2 = df_select[df_select['Place'].isin(place_list_day2)]
    df_target_day2 = df_target[df_target['Place'].isin(place_list_day2)]

    st.write ('Output Line Chart 📈: Target Revenues')

    highlight = alt.selection(type='single', on='mouseover',
                          fields=['Place'], nearest=True, empty="none")

    base = alt.Chart(df_target_day2).encode(
        x= alt.X('Date_time:T', axis = alt.Axis(labelAngle = 290, format = ("%d.%m.%H:%M"))),
        y = alt.Y('Revenue:Q'),
        color=alt.Color('Place:N', scale=alt.Scale(scheme='tableau20'), legend=alt.Legend(
              columns = 2,
              title = 'Retail Outlets'))).properties(height=410)
          
    points = base.mark_circle().encode(
        size = alt.value(0),
        opacity=alt.value(0),
        tooltip=['Place', alt.Tooltip('Revenue:Q',format=',.0f'), 'Date_time']
    ).add_selection(
        highlight
    ).properties(height=410)

    lines = base.mark_line().encode(
        size=alt.condition(~highlight, alt.value(0.5), alt.value(2))
    )
    st.altair_chart(points + lines, use_container_width=True)
    
    st.write ('Output Line Chart 📈: Predicted Revenues', fontSize = 8)
    pts = alt.selection(type="single", encodings=['x'])
    
    highlight = alt.selection(type='single', on='mouseover',
                          fields=['Place'], nearest=True, empty="none")

    base = alt.Chart(df_select_day2).encode(
        x= alt.X('Date_time:T', axis = alt.Axis(labelAngle = 290, format = ("%d.%m.%H:%M"))),
        y = alt.Y('Revenue:Q'),
        color=alt.Color('Place:N', scale=alt.Scale(scheme='tableau20'), legend=alt.Legend(
              columns = 2,
              title = 'Retail Outlets'))).properties(height=410)
          
    points = base.mark_circle().encode(
        size = alt.value(0),
        opacity=alt.value(0),
        tooltip=['Place', alt.Tooltip('Revenue:Q',format=',.0f'), 'Date_time']
    ).add_selection(
        highlight
    ).properties(height=410)

    lines = base.mark_line().encode(
        size=alt.condition(~highlight, alt.value(0.5), alt.value(2))
    )
    st.altair_chart(points + lines, use_container_width=True)
      
