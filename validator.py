import streamlit as st
import sqlite3
import pandas as pd
from streamlit_folium import st_folium
from utils import *

st.set_page_config(layout="wide")
st.title('data_validator')


col1, col2 = st.columns([0.4, 0.6] ,border=True, gap="small")
col3, col4 = st.columns([0.4, 0.6] ,border=True, gap="small")


with col1:
    with st.container(height=500, border=False):
        query = st.text_area(label = 'query',
                         value=
                         '''
                         SELECT * FROM pujo_data_6_9_2026
                         WHERE name IS NULL
                         ''')
        conn = sqlite3.connect('pujo_data.db')
        data = pd.read_sql(query,con=conn)
        row_num = st.number_input('select row',step =1)

        lat = data.loc[data.index[row_num], 'lat']
        lon = data.loc[data.index[row_num], 'lon']
        


with col2:
    with st.container(border=False):
        m = show_map(lat, lon)
        st_folium(m, width=None,height=400)
        bounds = [[(lat-0.0005), (lat+0.0005)],
                  [(lon-0.0005), (lon+0.0005)]]
        m.fit_bounds(bounds,padding=(1, 1))
        m.add_child(folium.LatLngPopup())
    #m.save("click_to_add.html")

    address = data_validator(lat, lon)
    st.write(address)

st.data_editor(data)