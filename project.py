import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

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
st.header('Features of the dataset:')
st.text('year, region: year and region')
st.text('wine: the number of litres of wine consumed in this year per person in this region')
st.text('beer: the number of litres of beer consumed in this year per person in this region')
st.text('vodka: the number of litres of vodka consumed in this year per person in this region')
st.text('champagne: the number of litres of champagne consumed in this year per person in this region')
st.text('brandy: the number of litres of brandy consumed in this year per person in this region')
st.header('Overview of the data')
df.iloc[:, 1:].describe(include=[np.number])
st.write(df)
mean_year = pd.DataFrame(
    [[year, df.loc[df['year'] == year]['wine'].mean(), df.loc[df['year'] == year]['beer'].mean(), df.loc[df['year'] == year]['vodka'].mean(), df.loc[df['year'] == year]['champagne'].mean(), df.loc[df['year'] == year]['brandy'].mean()] for year in range(1998, 2017)],
    columns = ['year', 'wine', 'beer', 'champagne', 'vodka', 'brandy']
)
mean_comparison_year = px.line(mean_year, x='year', y=['wine', 'beer', 'champagne', 'vodka', 'brandy'])
st.plotly_chart(mean_comparison_year)
