import streamlit as st
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import seaborn as sns
import altair as alt
from catboost import CatBoostRegressor, Pool

#CWD = f'/content/drive/MyDrive/Sherem_streamlit/'
#input_path = f'{CWD}input/'
#map_config = f'{CWD}map_config/'
#model_path = f'{CWD}models/'

count_may_pivot_rev = pd.read_csv ('./input/count_may_pivot_rev.csv')
count_june_pivot = pd.read_csv('./input/count_june_pivot.csv')

# Списки колонок
all_col_list = count_may_pivot_rev.columns[:-29].to_list()
weather_list = count_may_pivot_rev.columns[-31:-29].to_list()

date_list = count_may_pivot_rev.columns[-38:-31].to_list()
date_list.append(count_may_pivot_rev.columns[0])

general_list = count_may_pivot_rev.columns[-46:-42].to_list()
general_list.append(count_may_pivot_rev.columns[84])
general_perc_list = count_may_pivot_rev.columns[-42:-38].to_list()
count_list = count_may_pivot_rev.columns[1:84].to_list()
count_perc_list = count_may_pivot_rev.columns[85:-46].to_list()

aeroflot_ml_list = list(filter(lambda x: 'Aeroflot' in x, count_list))
aeroflot_ml_perc_list = list(filter(lambda x: 'Aeroflot' in x, count_perc_list))

pegas_ml_list = list(filter(lambda x: 'Pegas' in x, count_list))
pegas_ml_perc_list = list(filter(lambda x: 'Pegas' in x, count_perc_list))

X_all = count_may_pivot_rev [all_col_list]  
X_aeroflot = count_may_pivot_rev [date_list + general_list +general_perc_list +aeroflot_ml_list +aeroflot_ml_perc_list]
X_pegas = count_may_pivot_rev [date_list + general_list +general_perc_list +pegas_ml_list +pegas_ml_perc_list]
list_y = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '19', '21', '22', '23', '24', '25', '26', '27', '28']

# Загрузить модель All
model_all = CatBoostRegressor(iterations=1000,loss_function = "MultiRMSE",random_seed=43,logging_level='Silent')
model_all.load_model('./models/model_all')

# Загрузить модель Aeroflot
model_aeroflot = CatBoostRegressor(iterations=1000,loss_function = "MultiRMSE",random_seed=43,logging_level='Silent')
model_aeroflot.load_model('./models/model_aeroflot')

# Загрузить модель Pegas
model_pegas = CatBoostRegressor(iterations=1000,loss_function = "MultiRMSE",random_seed=43,logging_level='Silent')
model_pegas.load_model('./models/model_pegas')

# Написать функцию для создания "тепловых карт" корреляции
#@st.cache (suppress_st_warning=True)
def predict_rev_cor2(input_df,
                     X_col_input, input_list, input_model,
                     place_list, fig_height):
  pred_X_input_list = X_col_input.columns.to_list()
  preds = input_model.predict(input_df[pred_X_input_list])
  input_df[list_y] = preds
  solution_df = input_df[input_list + place_list]
  length = len(place_list)

  fig = plt.figure(figsize=(20, fig_height))
  ax = sns.heatmap(solution_df.corr()[-length:].T[:-length],
                   annot = True, cmap = 'YlGn', fmt=".2f",
                   vmin = -1, vmax = 1, linewidths = 0.1,
                   linecolor = 'white',
                   annot_kws={"size":12},
                   cbar=False)
  plt.tick_params(axis='both', which='major',
                  labelsize=10, labelbottom = False,
                  bottom=False, top = False, labeltop=True)
                  
  plt.xlabel('Retail Outlets Revenue \n ', fontsize=15)
  plt.ylabel('Traffic Features', fontsize=15)
  ax.xaxis.set_label_position('top')
  plt.tight_layout()
  #plt.show()
  st.pyplot(fig)

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
#st.markdown('# **Passenger Traffic Features and Revenues Correlation Matrices 🔁**')
st.markdown("<h1>Passenger Traffic Features and Revenue Correlation Matrices 🔁</h1>", unsafe_allow_html=True)
#st.markdown("\n\n")
# Selectbox
option = st.selectbox('Select Prediction Model ⚙️', ['All Features', 'Aeroflot', 'Pegas Fly'])

if option == "All Features":
  # Карта для модели All
  place_list_day = list_y
  place_list_day2 = st.multiselect('Select Retail Outlets 🛒', place_list_day, place_list_day)
  if not place_list_day2:
    st.error("Please select at least one retail outlet")
  else: 
    st.write ('Output Heatmap 🔥')

    predict_rev_cor2(input_df = count_june_pivot,
    X_col_input = X_all,
    input_list = all_col_list,
    input_model = model_all,
    place_list = place_list_day2,
    fig_height = 45)

elif option == "Aeroflot":
  place_list_day = list_y
  place_list_day2 = st.multiselect('Select Retail Outlets 🛒', place_list_day, place_list_day)
  if not place_list_day2:
    st.error("Please select at least one retail outlet")
  else:
    st.write ('Output Heatmap 🔥') 
    predict_rev_cor2(input_df = count_june_pivot,
    X_col_input = X_aeroflot,
    input_list = date_list + general_list +general_perc_list +aeroflot_ml_list +aeroflot_ml_perc_list,
    input_model = model_aeroflot,
    place_list = place_list_day2,
    fig_height = 35)

elif option == "Pegas Fly":
  place_list_day = list_y
  place_list_day2 = st.multiselect('Select Retail Outlets 🛒', place_list_day, place_list_day)
  if not place_list_day2:
    st.error("Please select at least one retail outlet")
  else: 
    st.write ('Output Heatmap 🔥')
    predict_rev_cor2(input_df = count_june_pivot,
    X_col_input = X_pegas,
    input_list = date_list +general_list +general_perc_list +pegas_ml_list +pegas_ml_perc_list,
    input_model = model_pegas,
    place_list = place_list_day2,
    fig_height = 5)




