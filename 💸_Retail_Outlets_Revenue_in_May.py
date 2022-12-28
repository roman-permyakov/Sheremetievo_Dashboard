import streamlit as st
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import seaborn as sns
import altair as alt
from streamlit_extras.metric_cards import style_metric_cards
import streamlit.components.v1 as components
import time
from streamlit_extras.app_logo import add_logo

# Стиль
def style_metric_cards(
    background_color: str = "#FFF",
    border_size_px: int = 1,
    border_color: str = "#CCC",
    border_radius_px: int = 5,
    border_left_color: str = "#48b6c7",
    box_shadow: bool = False,
):
    box_shadow_str = (
        "box-shadow: 0 0.15rem 1.75rem 0 rgba(58, 59, 69, 0.15) !important;"
        if box_shadow
        else "box-shadow: none !important;"
    )
    st.markdown(
        f"""
        <style>
            div[data-testid="metric-container"] {{
                background-color: {background_color};
                border: {border_size_px}px solid {border_color};
                padding: 5% 5% 5% 10%;
                border-radius: {border_radius_px}px;
                border-left: 0.5rem solid {border_left_color} !important;
                {box_shadow_str}
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

#CWD = https://drive.google.com/drive/folders/163SU8ySHLLkN007_hZLOCUTjadhklOZF
#input_path = f'/CWD/input/'

revenue_may = pd.read_excel ('./input/Revenue_may_clean.xlsx')
revenue_may_day_sum = revenue_may.groupby (by = ['Date', 'Place'],dropna = False)['Revenue'].sum().T.reset_index()
revenue_may_hour_sum = revenue_may.groupby (by = ['Time', 'Place'],dropna = False)['Revenue'].sum().T.reset_index()
revenue_may_hour_sum_copy = revenue_may_hour_sum.copy()

import streamlit as st

st.set_page_config(page_title='Forecasting the Revenue of Sheremetievo Airport Retail Outlets',
page_icon='https://alllogos.ru/images/logotip-sheremetevo.png', layout="wide")

# Sidebar Configuration
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

# Delete Burger Menu
#st.markdown(""" <style> MainMenu {visibility: hidden;} footer {visibility: hidden;} </style> """, unsafe_allow_html=True)

# New
st.markdown("<h1>Revenue of Sheremetievo Airport Retail Outlets 💸</h1>", unsafe_allow_html=True)
st.markdown('##### **Real Data. May, 2022**')
st.markdown("\n\n")


# Selectbox
option = st.selectbox(label = 'Select Type of Data Aggregation 📂', options = ['No Aggregation', 'Day Interval Aggregation', '30 Minutes Interval Aggregation during Day'])

if option == "No Aggregation":
  df_select = revenue_may
  df_select.Time = pd.to_datetime(df_select.Time)

  max_global_revenue = df_select['Revenue'].max()
  max_glo_revenue_line = df_select.loc[df_select['Revenue'] == max_global_revenue]
  max_global_place, max_global_date, max_global_time = max_glo_revenue_line['Place'].item(), max_glo_revenue_line['Date'].item(), max_glo_revenue_line['Time'].item()

  col1, col2, col3, col4 = st.columns(4)
  with col1:
    st.metric(label="Max Revenue", value = (str('{:,.0f}'.format(max_global_revenue) + ' ' + '₽')))
  with col2:
    st.metric(label="Retail Outlet", value = ('№ ' + str('{:.0f}'.format(max_global_place))))
  with col3:
    st.metric(label="Date", value = '{:%d-%m-%y}'.format(max_global_date))
  with col4:
    st.metric(label="Time", value = '{:%H:%M}'.format(max_global_time))
  style_metric_cards()

# Selection for a specific time frame.
  df_select = revenue_may 

  col1, col2 = st.columns(2)

  with col1:
      start_date = st.date_input('Select Start Date 📅',min_value= datetime.date(2022,5,1),max_value=datetime.date(2022,5,30),value=datetime.date(2022,5,1))

  with col2:    
      end_date = st.date_input('Select End Date 📅',min_value=datetime.date(2022,5,2),max_value=datetime.date(2022,5,31),value=datetime.date(2022,5,31))

  if(start_date != None or end_date != None):
      if(start_date < end_date):
          s1 = datetime.datetime.combine(start_date, datetime.time.min)
          s2 = datetime.datetime.combine(end_date, datetime.time.min)
          df_select = revenue_may[(revenue_may['Date'] >= s1) & (revenue_may['Date']<= s2)]
      else:
          st.warning("Invalid Date Range - Re-enter Dates")

  # Graphs and charts for selected date range.
  place_list = df_select['Place'].unique()
  place_list.sort()
  place_list_2 = st.multiselect('Select Retail Outlets 🛒', place_list, place_list)

  if not place_list_2:
    st.error("Please select at least one retail outlet")
  else: 
    df_select_2 = df_select[df_select['Place'].isin(place_list_2)]
    df_select_2.rename(columns={'Place': 'Retail Outlet'}, inplace = True)
    df_select_3 = df_select_2 [['Date_time', 'Retail Outlet', 'Revenue']].sort_values(by = ['Date_time', 'Retail Outlet']).reset_index()
    df_select_3.drop(['index'], axis = 1, inplace = True)
    df_select_3.Date_time = pd.to_datetime(df_select_3.Date_time)

    df_select_3['Revenue'] = df_select_3['Revenue'].map('{:,.0f}'.format)
    df_select_3['Date_time'] = df_select_3['Date_time'].map('{:%d.%m.%Y.%H:%M}'.format) 
    
    #components.html("""<h6 style="font-size:4px; font-weight: lighter">Output Table 📝</h6>""")
    st.write("Output Table 📝")
    
    st.dataframe(df_select_3, width=None, height=178, use_container_width=True)

    st.write ('Output Line Chart 📈')
  
    base = alt.Chart(df_select_2).mark_rule(size=1.4).encode(
        x= alt.X ('Date_time:T', axis = alt.Axis(labelAngle = 290, format = ("%d.%m.%H:%M"))),
        y= alt.Y ('Revenue:Q'),
        color=alt.Color('Retail Outlet:N', scale=alt.Scale(scheme='tableau20'), legend=alt.Legend(
            columns = 2,
            title = 'Retail Outlets')))
    
    st.altair_chart(base, use_container_width=True)
    
# Selectbox (2)    
elif option == "Day Interval Aggregation":
  df_select = revenue_may_day_sum

  max_global_revenue = df_select['Revenue'].max()
  max_glo_revenue_line = df_select.loc[df_select['Revenue'] == max_global_revenue]
  max_global_place, max_global_date = max_glo_revenue_line['Place'].item(), max_glo_revenue_line['Date'].item()

  col1, col2, col3, col4 = st.columns(4)
  with col1:
    st.metric(label="Max Revenue", value = (str('{:,.0f}'.format(max_global_revenue) + ' ' + '₽')))
  with col2:
    st.metric(label="Retail Outlet", value = ('№ ' + str('{:.0f}'.format(max_global_place))))
  with col3:
    st.metric(label="Date", value = '{:%d-%m-%y}'.format(max_global_date))
  style_metric_cards()
  with col4:
    st.write(label='', value = '')
  

# Selection for a specific time frame.
  df_select_day = revenue_may_day_sum 

  col1, col2 = st.columns(2)

  with col1:
    start_date1 = st.date_input('Select Start Date 📅',min_value= datetime.date(2022,5,1),max_value=datetime.date(2022,5,30),value=datetime.date(2022,5,1))
  
  with col2:
    end_date1 = st.date_input('Select End Date 📅',min_value=datetime.date(2022,5,2),max_value=datetime.date(2022,5,31),value=datetime.date(2022,5,31))

  if(start_date1 != None or end_date1 != None):
    if(start_date1 < end_date1):
      s3 = datetime.datetime.combine(start_date1, datetime.time.min)
      s4 = datetime.datetime.combine(end_date1, datetime.time.min)
      df_select_day = revenue_may_day_sum [(revenue_may_day_sum ['Date'] >= s3) & (revenue_may_day_sum ['Date']<= s4)]
    else:
      st.warning("Invalid Date Range - Re-enter Dates")

  # Graphs and charts for selected date range.
  place_list_day = df_select_day['Place'].unique()
  place_list_day.sort()
  place_list_day2 = st.multiselect('Select Retail Outlet 🛒', place_list_day, place_list_day)
  if not place_list_day2:
    st.error("Please select at least one retail outlet")
  else: 
    df_select_day2 = df_select_day[df_select_day['Place'].isin(place_list_day2)]
    df_select_day2.rename(columns={'Place': 'Retail Outlet'}, inplace = True)
    df_select_3 = df_select_day2 [['Date', 'Retail Outlet', 'Revenue']].sort_values(by = ['Date', 'Retail Outlet'])
    df_select_3.Date = pd.to_datetime(df_select_3.Date)

    df_select_3['Revenue'] = df_select_3['Revenue'].map('{:,.0f}'.format)
    df_select_3['Date'] = df_select_3['Date'].map('{:%d.%m.%Y}'.format) 

    st.write ('Output Table 📝')
    st.dataframe(df_select_3, width=None, height=178, use_container_width=True)
    
    st.write ('Output Line Chart 📈')
  
    highlight = alt.selection(type='single', on='mouseover',
                          fields=['Retail Outlet'], nearest=True, empty="none")

    base = alt.Chart(df_select_day2).encode(
        x= alt.X('Date:T', axis = alt.Axis(labelAngle = 290, format = ("%d.%m"))),
        y = alt.Y('Revenue:Q'),
        color=alt.Color('Retail Outlet:N', scale=alt.Scale(scheme='tableau20'), legend=alt.Legend(
              columns = 2,
              title = 'Retail Outlets'))).properties(height=410)
          
    points = base.mark_circle().encode(
        size = alt.value(0),
        opacity=alt.value(0),
        tooltip=['Retail Outlet', alt.Tooltip('Revenue:Q',format=',.0f'), 'Date']
    ).add_selection(
        highlight
    ).properties(height=410)

    lines = base.mark_line().encode(
        size=alt.condition(~highlight, alt.value(0.8), alt.value(2))
    )
    st.altair_chart(points + lines, use_container_width=True)

# Selectbox (3)    
elif option == "30 Minutes Interval Aggregation during Day":
  df_select = revenue_may_hour_sum
  df_select.Time = pd.to_datetime(df_select.Time)

  max_global_revenue = df_select['Revenue'].max()
  max_glo_revenue_line = df_select.loc[df_select['Revenue'] == max_global_revenue]
  max_global_place, max_global_time = max_glo_revenue_line['Place'].item(), max_glo_revenue_line['Time'].item()

  col1, col2, col3, col4 = st.columns(4)
  with col1:
    st.metric(label="Max Revenue", value = (str('{:,.0f}'.format(max_global_revenue) + ' ' + '₽')))
  with col2:
    st.metric(label="Retail Outlet", value = ('№ ' + str('{:.0f}'.format(max_global_place))))
  with col3:
    st.metric(label="Time", value = '{:%H:%M}'.format(max_global_time))
  with col4:
    st.write(label='', value = '')
  style_metric_cards()

# Selection for a specific time frame.
  revenue_may_hour_sum.Time = pd.to_datetime(revenue_may_hour_sum.Time)
  revenue_may_hour_sum['Time_3'] = revenue_may_hour_sum['Time'] - pd.Timedelta(hours=3)
  
  df_select_hour = revenue_may_hour_sum
  
  # Graphs and charts for selected date range.
  place_list_hour = revenue_may_hour_sum['Place'].unique()
  place_list_hour.sort()
  place_list_hour3 = st.multiselect('Select Retail Outlet 🛒', place_list_hour, place_list_hour)
  if not place_list_hour3:
    st.error("Please select at least one retail outlet")
  else: 
    df_select_hour2 = revenue_may_hour_sum[revenue_may_hour_sum['Place'].isin(place_list_hour3)]
    df_select_hour2.rename(columns={'Place': 'Retail Outlet'}, inplace = True)
    df_select_3 = df_select_hour2 [['Time', 'Retail Outlet', 'Revenue']].sort_values(by = ['Time', 'Retail Outlet'])
    df_select_3.Time = pd.to_datetime(df_select_3.Time)
   
    df_select_3['Revenue'] = df_select_3['Revenue'].map('{:,.0f}'.format)
    df_select_3['Time'] = df_select_3['Time'].map('{:%H:%M}'.format) 

    st.write ('Output Table 📝')
    st.dataframe(df_select_3, width=None, height=178, use_container_width=True)
    
    st.write ('Output Line Chart 📈')
    

    highlight3 = alt.selection(type='single', on='mouseover', fields=['Retail Outlet'], nearest=True, empty="none")

    base = alt.Chart(df_select_hour2).encode(
      x = alt.X('Time_3:T',axis = alt.Axis(labelAngle = 290, format = ("%H:%M")), title = 'Time'),
      y = alt.Y('Revenue:Q'),
      color=alt.Color('Retail Outlet:N', scale=alt.Scale(scheme='tableau20'), legend=alt.Legend(
        columns = 2,
        title = 'Retail Outlets'))).properties(height=410)
          
    points = base.mark_circle().encode(
      size = alt.value(0),
      opacity=alt.value(0),
      tooltip=['Retail Outlet', alt.Tooltip('Revenue:Q',format=',.0f'), alt.Tooltip('Time_3:T',format='%H:%M', title = 'Time')]).add_selection(highlight3
    ).properties(height=410)

    lines = base.mark_line().encode(size=alt.condition(~highlight3, alt.value(0.8), alt.value(2)))
    st.altair_chart(points + lines, use_container_width=True)