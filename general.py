import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import numpy as np

st.title('Alcohol Consumption in Russia (1998 - 2016)')
st.header('The dataset includes information on consumption of five different types of alcohol (beer, wine, vodka, brandy, champagne) in different regions of Russia over the period betwenn 1998 and 2016')
st.subheader('Firstly I installed and imported all the libraries I was going to use')
st.code(r'''import pandas as pd
import plotly.express as px
import folium
import requests
import geopandas as gpd
import numpy as np''')
st.header('Data Cleanup')
st.code(r'''df = pd.read_csv('russia_alcohol.csv')
df.info''')
