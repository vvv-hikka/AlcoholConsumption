import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as plt

st.title('Alcohol Consumption in Russia (1998 - 2016)')
st.header('This dashboard will present the information about alcohol consumption in Russia between 1998 and 2016')
st.text("Let's display my dataset")
st.code(r'''df = pd.read_csv('russia_alcohol.csv')
df = df.drop(df.loc[(df['region'] == 'Sevastopol') | (df['region'] == 'Chechen Republic') | (df['region'] == 'Republic of Crimea') | (df['region'] == 'Republic of Ingushetia')].index)
df['total_eth'] = 0.05 * df['beer'] + 0.13 * df['wine'] + 0.4 * df['vodka'] + 0.4 * df['brandy'] + 0.12 * df['champagne']
df['total_litres'] = df['beer'] + df['wine'] + df['champagne'] + df['brandy'] + df['vodka']
df''')
df = pd.read_csv('russia_alcohol.csv')
df = df.drop(df.loc[(df['region'] == 'Sevastopol') | (df['region'] == 'Chechen Republic') | (df['region'] == 'Republic of Crimea') | (df['region'] == 'Republic of Ingushetia')].index)
df['total_eth'] = 0.05 * df['beer'] + 0.13 * df['wine'] + 0.4 * df['vodka'] + 0.4 * df['brandy'] + 0.12 * df['champagne']
df['total_litres'] = df['beer'] + df['wine'] + df['champagne'] + df['brandy'] + df['vodka']
if st.checkbox('Show dataframe'):
   st.write(df)
