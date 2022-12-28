import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import seaborn as sns
import altair as alt
from streamlit_extras.metric_cards import style_metric_cards

# Стиль
def style_metric_cards(
    background_color: str = "#FFF",
    border_size_px: int = 1,
    border_color: str = "#CCC",
    border_radius_px: int = 5,
    border_left_color: str = "#48b6c7", #48b6c7 #9AD8E1
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
#CWD = f'/content/drive/MyDrive/Sherem_streamlit/'
#input_path = f'{CWD}input/'

# Загрузить данные пассажиропотока в мае-июне
pass_all = pd.read_csv ('./input/pass_all_clean.csv')
pass_all['Flight_Date']=pd.to_datetime(pass_all.Flight_Date)
pass_all['EntryFlight_Time']=pd.to_datetime(pass_all.EntryFlight_Time)
pass_all2 = pass_all.copy()
pass_all2['Time'] = pass_all2['EntryFlight_Time'].apply(lambda x: x.strftime('%H:%M'))
pass_all2_hour_sum = pass_all2.groupby(by = ['Time'],dropna = False)['Terminal'].agg(['count']).reset_index()

# Считаем число пассажиров по дням
pass_all_group_date = pass_all.groupby(by = ['Flight_Date', 'Airline_Name'],dropna = False)['Terminal'].agg(['count']).reset_index()
pass_all_group_date2 = pass_all.groupby(by = ['Flight_Date'],dropna = False)['Terminal'].agg(['count']).reset_index()
pass_date_merged = pass_all_group_date.merge(pass_all_group_date2, left_on='Flight_Date', right_on='Flight_Date')
#pass_date_merged.rename(columns={'count_x': 'Selected_Airline_count', 'count_y': 'All_Airlines_count'}, inplace=True)

max_global_count = pass_date_merged['count_x'].max()
max_glo_count_line = pass_date_merged.loc[pass_date_merged['count_x'] == max_global_count]
max_global_airline, max_global_date = max_glo_count_line['Airline_Name'].item(), max_glo_count_line['Flight_Date'].item()

# Считаем число пассажиров последовательно по времени
pass_all_group_time = pass_all.groupby(by = ['EntryFlight_Time', 'Airline_Name'],dropna = False)['Terminal'].agg(['count']).reset_index()

max_time_count = pass_all_group_time['count'].max()
max_time_count_line = pass_all_group_time.loc[pass_all_group_time['count'] == max_time_count]
max_time_airline, max_time_time = max_time_count_line['Airline_Name'].item(), max_time_count_line['EntryFlight_Time'].item()

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
#st.markdown('# **Passenger Traffic Time Aggregation 🕐**')
st.markdown("<h1>Passenger Traffic Time Aggregation 🕐</h1>", unsafe_allow_html=True)
st.markdown('##### **Real Data. May-June, 2022**')
st.markdown("\n\n")

# Selectbox
option = st.selectbox('Select Type of Data Aggregation 📂', ['No Aggregation', 'Day Interval Aggregation', 'Minute Interval Aggregation during Day' ])

if option == "No Aggregation":

  col1, col2, col3, col4 = st.columns(4)
  with col1:
    st.metric(label="Max Count", value = (str('{:,.0f}'.format(max_time_count))))
  with col2:
    st.metric(label="Airline", value = max_time_airline)
  with col3:
    st.metric(label="Date", value = '{:%d-%m-%y}'.format(max_time_time))
  with col4:
    st.metric(label="Time", value = '{:%H:%M}'.format(max_time_time))
  style_metric_cards()

  # Selection for a specific time frame.
  df_select = pass_all_group_time
  df_select.EntryFlight_Time = pd.to_datetime(df_select.EntryFlight_Time)

  col1, col2 = st.columns(2)

  with col1:
      start_date = st.date_input('Select Start Date 📅',min_value= datetime.date(2022,5,1),max_value=datetime.date(2022,6,29),value=datetime.date(2022,5,1))

  with col2:    
      end_date = st.date_input('Select End Date 📅',min_value=datetime.date(2022,5,2),max_value=datetime.date(2022,6,30),value=datetime.date(2022,6,30))

  if(start_date != None or end_date != None):
      if(start_date < end_date):
          s1 = datetime.datetime.combine(start_date, datetime.time.min)
          s2 = datetime.datetime.combine(end_date, datetime.time.min)
          df_select = pass_all_group_time[(pass_all_group_time['EntryFlight_Time'] >= s1) & (pass_all_group_time['EntryFlight_Time']<= s2)]
      else:
          st.warning("Invalid Date Range - Re-enter Dates")  
  
  # Graphs and charts for selected date range.
  airlines_list = df_select['Airline_Name'].unique()
  airlines_list.sort()
  airlines_list_2 = st.multiselect('Select Airlines ✈️', airlines_list, airlines_list)

  if not airlines_list_2:
    st.error("Please select at least one airlines")
  else: 
    df_select_2 = df_select[df_select['Airline_Name'].isin(airlines_list_2)]

    st.write("Output Table 📝")
    df_select_2_new = df_select_2.rename(columns={'Airline_Name': 'Airlines', 'count': 'Passengers', 'EntryFlight_Time': 'Boarding Time'})
    df_select_2_new['Boarding Time'] = df_select_2_new['Boarding Time'].map('{:%d.%m.%Y.%H:%M}'.format) 
    st.dataframe(df_select_2_new, width=None, height=178, use_container_width=True)

    st.write ('Output Line Chart 📈')

    
    highlight = alt.selection(type='single', on='mouseover',
                          fields=['Airline_Name'], nearest=True, empty="none")

    domain = ["Aeroflot","Ariana Afghan Airlines","Cham Wings Airlines","Corendon Airlines","Etihad Airways",
    "JAT Airways","Mahan Air","Nordavia","Nordwind Airlines","Pegas Fly","Red Wings","Rossiya","Severstal"]
    range_ = [ '#48b6c7', '#1f77b4', '#ff7f0e', '#aec7e8', '#ffbb78', '#2ca02c', '#98df8a', '#c5b0d5',  '#8c564b', 
    '#9467bd', '#d62728', '#ff9896', '#c49c94']                        

    base = alt.Chart(df_select_2).encode(
        x= alt.X('EntryFlight_Time:T', title = 'Boarding Time', axis = alt.Axis(labelAngle = 290, format = ("%d.%m.%H:%M"))),
        y = alt.Y('count:Q', title = 'Passengers'),
        color=alt.Color('Airline_Name:O', scale=alt.Scale(domain=domain, range=range_), legend=alt.Legend(
              columns = 1,
              title = 'Airlines'))).properties(height=410)
          
    points = base.mark_circle().encode(
        size = alt.value(0),
        opacity=alt.value(0),
        tooltip=['Airline_Name:O', alt.Tooltip('count:Q',format=',.0f', title = "Passengers"), alt.Tooltip('EntryFlight_Time:T', format = ("%d.%m.%H:%M"), title = "Boarding Time")]
    ).add_selection(
        highlight
    ).properties(height=410)

    lines = base.mark_line().encode(
        size=alt.condition(~highlight, alt.value(0.8), alt.value(2))
    )
    st.altair_chart(points + lines, use_container_width=True)
    
    st.write ('Output Bar Chart 📊')
    domain = ["Aeroflot","Ariana Afghan Airlines","Cham Wings Airlines","Corendon Airlines","Etihad Airways",
    "JAT Airways","Mahan Air","Nordavia","Nordwind Airlines","Pegas Fly","Red Wings","Rossiya","Severstal"]
    range_ = [ '#48b6c7', '#1f77b4', '#ff7f0e', '#aec7e8', '#ffbb78', '#2ca02c', '#98df8a', '#c5b0d5',  '#8c564b', 
    '#9467bd', '#d62728', '#ff9896', '#c49c94']  

    #click = alt.selection_multi(encodings=['color'])
    c = alt.Chart(df_select_2).mark_bar(size = 5).encode(
    y= alt.Y ('sum(count)', stack='zero',title = 'Passengers'),
    color=alt.Color('Airline_Name:O', sort=['x', 'Airline_Name'], scale=alt.Scale(domain=domain, range=range_), legend=alt.Legend(title = 'Airlines')),
    x= alt.X ('EntryFlight_Time:T', sort=['-x', 'count'], title = 'Boarding Time', axis = alt.Axis(labelAngle = 290, format = ("%d.%m.%H:%M"))),
    #color = alt.condition(click, color, alt.value('lightgray')),
    opacity=alt.value(0.6)).properties()#.add_selection(click)

    st.altair_chart(c, use_container_width=True)    

elif option == "Day Interval Aggregation":

  col1, col2, col3, col4 = st.columns(4)
  with col1:
    st.metric(label="Max Count", value = (str('{:,.0f}'.format(max_global_count))))
  with col2:
    st.metric(label="Airline", value = max_global_airline)
  with col3:
    st.metric(label="Flight_Date", value = '{:%d-%m-%y}'.format(max_global_date))
  with col4:
    st.write(label=" ", value = '')
  style_metric_cards()

  # Selection for a specific time frame.
  df_select = pass_date_merged
  df_select.Flight_Date = pd.to_datetime(df_select.Flight_Date) 

  col1, col2 = st.columns(2)

  with col1:
      start_date = st.date_input('Select Start Date 📅',min_value= datetime.date(2022,5,1),max_value=datetime.date(2022,6,29),value=datetime.date(2022,5,1))

  with col2:    
      end_date = st.date_input('Select End Date 📅',min_value=datetime.date(2022,5,2),max_value=datetime.date(2022,6,30),value=datetime.date(2022,6,30))

  if(start_date != None or end_date != None):
      if(start_date < end_date):
          s1 = datetime.datetime.combine(start_date, datetime.time.min)
          s2 = datetime.datetime.combine(end_date, datetime.time.min)
          df_select = pass_date_merged[(pass_date_merged['Flight_Date'] >= s1) & (pass_date_merged['Flight_Date']<= s2)]
      else:
          st.warning("Invalid Date Range - Re-enter Dates")

  # Graphs and charts for selected date range.
  airlines_list = df_select['Airline_Name'].unique()
  airlines_list.sort()
  airlines_list_2 = st.multiselect('Select Airlines ✈️', airlines_list, airlines_list)

  if not airlines_list_2:
    st.error("Please select at least one airlines")
  else: 
    df_select_2 = df_select[df_select['Airline_Name'].isin(airlines_list_2)]

    st.write("Output Table 📝")
    df_select_2_new = df_select_2.rename(columns={'Airline_Name': 'Airlines', 'count_x': 'Passengers'})
    df_select_2_new = df_select_2_new [['Flight_Date', 'Airlines', 'Passengers']]
    df_select_2_new['Flight_Date'] = df_select_2_new['Flight_Date'].map('{:%d.%m.%Y}'.format) 
    st.dataframe(df_select_2_new, width=None, height=178, use_container_width=True)

    st.write ('Output Line Chart 📈')
    highlight = alt.selection(type='single', on='mouseover',
                          fields=['Airline_Name'], nearest=True, empty="none")

    domain = ["Aeroflot","Ariana Afghan Airlines","Cham Wings Airlines","Corendon Airlines","Etihad Airways",
    "JAT Airways","Mahan Air","Nordavia","Nordwind Airlines","Pegas Fly","Red Wings","Rossiya","Severstal"]
    range_ = [ '#48b6c7', '#1f77b4', '#ff7f0e', '#aec7e8', '#ffbb78', '#2ca02c', '#98df8a', '#c5b0d5',  '#8c564b', 
    '#9467bd', '#d62728', '#ff9896', '#c49c94']   

    base = alt.Chart(df_select_2).encode(
        x= alt.X('Flight_Date:T', axis = alt.Axis(labelAngle = 290, format = ("%d.%m"))),
        y = alt.Y('count_x:Q', title = 'Passengers'),
        color=alt.Color('Airline_Name:O', scale=alt.Scale(domain=domain, range=range_), legend=alt.Legend(
              columns = 1,
              title = 'Airlines'))).properties(height=410)
          
    points = base.mark_circle().encode(
        size = alt.value(0),
        opacity=alt.value(0),
        tooltip=['Airline_Name:O', alt.Tooltip('count_x:Q',format=',.0f', title = "Sel.Airline_Pass Count"), 'Flight_Date']
    ).add_selection(
        highlight
    ).properties(height=410)

    lines = base.mark_line().encode(
        size=alt.condition(~highlight, alt.value(0.8), alt.value(2))
    )
    st.altair_chart(points + lines, use_container_width=True)

    st.write ('Output Bar Chart 📊')
    domain = ["Aeroflot","Ariana Afghan Airlines","Cham Wings Airlines","Corendon Airlines","Etihad Airways",
    "JAT Airways","Mahan Air","Nordavia","Nordwind Airlines","Pegas Fly","Red Wings","Rossiya","Severstal"]
    range_ = [ '#48b6c7', '#1f77b4', '#ff7f0e', '#aec7e8', '#ffbb78', '#2ca02c', '#98df8a', '#c5b0d5',  '#8c564b', 
    '#9467bd', '#d62728', '#ff9896', '#c49c94']

    #click = alt.selection_multi(encodings=['color'])
    c = alt.Chart(df_select_2).mark_bar().encode(
    y= alt.Y ('sum(count_x)', stack='zero', title = 'Passengers'),
    x= alt.X ('Flight_Date:T', sort=['-x', 'count'], axis = alt.Axis(labelAngle = 290, format = ("%d.%m"))),
    color=alt.Color('Airline_Name:O', sort=['x', 'Airline_Name'], scale=alt.Scale(domain=domain, range=range_), legend=alt.Legend(title = 'Airlines')),
    tooltip=['Airline_Name:O', alt.Tooltip('count_x:Q',format=',.0f', title = "Sel.Airline_Pass Count"), alt.Tooltip('count_y:Q',format=',.0f', title = "All.Airline_Pass Count"), 'Flight_Date'],
    #color=alt.condition(click, color, alt.value('lightgray')),
    opacity=alt.value(0.6)).properties()#.add_selection(click)
    st.altair_chart(c, use_container_width=True)

elif option == "Minute Interval Aggregation during Day":
  df_select = pass_all2_hour_sum
  #df_select.Time = pd.to_datetime(df_select.Time)

  max_count_30min = df_select['count'].max()
  max_count_line = df_select.loc[df_select['count'] == max_count_30min]
  max_count_time = max_count_line['Time'].item()

  col1, col2, col3, col4 = st.columns(4)
  with col1:
    st.metric(label="Max Count", value = (str('{:,.0f}'.format(max_count_30min))))
  with col2:
    st.metric(label="Time", value = max_count_time)
  with col3:
    st.write(label=" ", value = '')
  with col4:
    st.write(label=" ", value = '')
  style_metric_cards()

  # Selection for a specific time frame.
  df_select = pass_all2_hour_sum
  st.write("Output Table 📝")
  df_select = df_select.rename(columns={'count': 'Passengers'})
  #df_select_2_new = df_select_2_new [['Flight_Date', 'Airlines', 'Passengers']]
  #df_select['Passengers'] = df_select['Passengers'].map('{:,.0f}'.format) 
  st.dataframe(df_select, width=None, height=178, use_container_width=True)

  st.write ('Output Line Chart 📈')
  highlight = alt.selection(type='single', on='mouseover',
                          fields=['Passengers'], nearest=True, empty="none")

  base = alt.Chart(df_select).mark_line().encode(
      x = alt.X('Time:O', axis = alt.Axis(labelAngle = 290)),
      y = alt.Y('Passengers:Q', title = 'Passengers'),
      color=alt.value('#48b6c7')).properties()

  points = base.mark_circle().encode(
        size = alt.value(0),
        opacity=alt.value(0),
        tooltip=['Time:O', alt.Tooltip('Passengers:Q',format=',.0f', title = "Passengers Count"), ]).add_selection(
        highlight).properties(height=410)
          
  st.altair_chart(points + base, use_container_width=True)
    
    



  