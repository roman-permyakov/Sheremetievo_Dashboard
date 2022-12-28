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

rev_merged = revenue_june_target.merge(revenue_june_predict_all, left_on=['Date_time', 'Place'], right_on=['Date_time', 'Place']).sort_values(by = ['Place'])
rev_merged.rename(columns={'Revenue_x': 'Target', 'Revenue_y': 'Prediction_All_Features'}, inplace = True)
rev_merged2 = rev_merged.merge(revenue_june_predict_aeroflot, left_on=['Date_time', 'Place'], right_on=['Date_time', 'Place']).sort_values(by = ['Place'])
rev_merged2.rename(columns={'Revenue': 'Prediction_Aeroflot'}, inplace = True)
rev_merged3 = rev_merged2.merge(revenue_june_predict_pegas, left_on=['Date_time', 'Place'], right_on=['Date_time', 'Place']).sort_values(by = ['Place'])
rev_merged3.rename(columns={'Revenue': 'Prediction_Pegas'}, inplace = True)
rev_merged4 = rev_merged3 [['Date_time', 'Place', 'Target', 'Prediction_All_Features', 'Prediction_Aeroflot', 'Prediction_Pegas']].sort_values(by = ['Date_time', 'Place'])
rev_merged4.rename(columns={'Place': 'Retail Outlet',}, inplace = True)

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
#st.markdown('# **Comparison of Prediction Models per Retail Point 🛒**')
st.markdown("<h1>Comparison of Prediction Models per Retail Outlet 🛒</h1>", unsafe_allow_html=True)
st.markdown("\n\n")

# Selectbox
# Selection for a specific time frame.

df_select = rev_merged4

col1, col2 = st.columns(2)

with col1:
  start_date = st.date_input('Select Start Date 📅',min_value= datetime.date(2022,6,1),max_value=datetime.date(2022,6,29),value=datetime.date(2022,6,1))
with col2:    
  end_date = st.date_input('Select End Date 📅',min_value=datetime.date(2022,6,2),max_value=datetime.date(2022,6,30),value=datetime.date(2022,6,30))

if(start_date != None or end_date != None):
  if(start_date < end_date):
      s1 = datetime.datetime.combine(start_date, datetime.time.min)
      s2 = datetime.datetime.combine(end_date, datetime.time.min)
      df_select = rev_merged4[(rev_merged4['Date_time'] >= s1) & (rev_merged4['Date_time']<= s2)]
  else:
      st.warning("Invalid Date Range - Re-enter Dates")  
  
  
# Graphs and charts for selected date range.
place_list_day = df_select['Retail Outlet'].unique()
place_list_day.sort()
option = st.selectbox('Select Retail Outlet 🛒', place_list_day, key='Place')

if not option:
  st.error("Please select at least one retail outlet")
else:
  df_select_day2 = df_select[df_select['Retail Outlet'].isin([option])]
  df_select_day3 = df_select_day2 [['Date_time', 'Target', 'Prediction_All_Features', 'Prediction_Aeroflot', 'Prediction_Pegas']]
  df_select_day3.set_index(['Date_time'], inplace = True)
  data = df_select_day3.reset_index().melt('Date_time')
  data.rename(columns={'variable': 'Model'}, inplace = True)

  cols_1_extract = df_select_day2.columns[:1]
  df_select_day2[cols_1_extract] = df_select_day2[cols_1_extract].applymap('{:%d.%m.%Y.%H:%M}'.format) 

  cols_2_extract = df_select_day2.columns[2:]
  df_select_day2[cols_2_extract] = df_select_day2[cols_2_extract].applymap('{:,.1f}'.format)
  
  st.write ('Output Table 📝')
  st.dataframe(df_select_day2, width=None, height=178, use_container_width=True)  
  
  domain = ['Target', 'Prediction_All_Features', 'Prediction_Aeroflot', 'Prediction_Pegas' ]
  range_ = ['#ff9896', '#98df8a', '#48b6c7', '#9467bd']

  base = alt.Chart(data).encode(x='Date_time:T')
  columns = sorted(data.Model.unique())

  st.write ('Output Line Chart 📈')
  selection = alt.selection_single(nearest=True, on='mouseover',
                        fields=['Date_time'], empty='none', clear='mouseout')
  
  lines = base.mark_line(size = 0.8).encode(
    x= alt.X ('Date_time', axis = alt.Axis(labelAngle = 290, format = ("%d.%m.%H:%M"))),
    y= alt.Y ('value:Q', title = 'Revenue'),
    color = alt.Color('Model:N', scale=alt.Scale(domain=domain, range=range_)))

  points = lines.mark_point().transform_filter(selection)

  rules = base.transform_pivot(
    'Model', value='value', groupby=['Date_time']).mark_rule().encode(
    opacity=alt.condition(selection, alt.value(0.3), alt.value(0)),
    tooltip=[alt.Tooltip(c, type='quantitative') for c in columns]).add_selection(selection)

  st.altair_chart(lines + points + rules, use_container_width=True)
  
