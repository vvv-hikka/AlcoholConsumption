from flask import Flask, render_template, request, send_file
import pandas as pd
import plotly.express as px
import os
import plotly
import base64


df = pd.read_csv('russia_alcohol.csv')
df = df.drop(df.loc[(df['region'] == 'Sevastopol') | (df['region'] == 'Chechen Republic') | (df['region'] == 'Republic of Crimea') | (df['region'] == 'Republic of Ingushetia')].index)
df['total_eth'] = 0.05 * df['beer'] + 0.13 * df['wine'] + 0.4 * df['vodka'] + 0.4 * df['brandy'] + 0.12 * df['champagne']
app = Flask(__name__)


@app.route('/')
def index():
    regions = list(df['region'].unique())
    return render_template('index.html', regions=regions)


@app.route('/process', methods=['POST'])
def start():
    region = request.form['regions']
    region_mod = ''.join(region.split())
    if not os.path.exists('static/images'):
        os.makedirs('static/images')
    path_line = f'static/images/{region_mod}_line.jpeg'
    path_pie = f'static/images/{region_mod}_pie.jpeg'
    path_comp = f'static/images/{region_mod}_comp.jpeg'
    line_src = line_graph(region, path_line)
    table_src = table(region)
    av_str_src = average_structure(region, path_pie)
    comp_src = comparison_line(region, path_comp)
    return render_template('index.html', regions=list(df['region'].unique()), selected_region=region, img_line=line_src, html_table = table_src, img_str=av_str_src, img_comp_time=comp_src)


def comparison_line(region, path_comp):
    if not os.path.exists(path_comp):
        comp_df = df.loc[(df['region'] == 'Moscow') | (df['region'] == 'Moscow Oblast') | (df['region'] == 'Krasnodar Krai') | (df['region'] == 'Saint Petersburg') | (df['region'] == 'Sverdlovsk Oblast') | (df['region'] == region)]
        comp_line = px.line(comp_df, x='year', y='total_eth', color='region')
        try:
            comp_line.write_image(path_comp,  engine='kaleido')
        except Exception as e:
            print(f"Error saving image for {region}: {e}")
    with open(path_comp, 'rb') as img_file:
        comp_data = base64.b64encode(img_file.read()).decode('utf-8')
    comp_src = f'data:image/jpeg;base64,{comp_data}'
    return comp_src


def average_structure(region, path_bar):
    if not os.path.exists(path_bar):
        one_region = df.loc[(df['region'] == region)]
        one_region_str = pd.DataFrame(
            [[drink, one_region[drink].mean()] for drink in {'wine', 'beer', 'vodka', 'champagne', 'brandy'}],
            columns=['drink', 'count']
        )
        pie_fig = px.pie(one_region_str, values='count', names='drink')
        try:
            pie_fig.write_image(path_bar, engine='kaleido')
        except Exception as e:
            print(f"Error saving image for {region}: {e}")
    with open(path_bar, 'rb') as img_file:
        pie_data = base64.b64encode(img_file.read()).decode('utf-8')
    av_str_src = f'data:image/jpeg;base64,{pie_data}'
    return av_str_src


def line_graph(region, path_line):
    if not os.path.exists(path_line):
        one_region = df.loc[(df['region'] == region)]
        line_fig = px.line(one_region, x='year', y=['wine', 'beer', 'vodka', 'champagne', 'brandy'])
        try:
            line_fig.write_image(path_line, engine='kaleido')
        except Exception as e:
            print(f"Error saving image for {region}: {e}")
    with open(path_line, 'rb') as img_file:
        line_data = base64.b64encode(img_file.read()).decode('utf-8')
    line_src = f'data:image/jpeg;base64,{line_data}'
    return line_src


def table(region):
    one_region = df.loc[(df['region']) == region]
    table_src = one_region.to_html()
    return table_src


@app.route('/second')
def second():
    years = list(df['year'].unique())
    return render_template('second.html', years=years)


@app.route('/second/process', methods=['post'])
def s_start():
    years = list(df['year'].unique())
    year = request.form['years']
    one_year = df.loc[(df['year'] == int(year))]
    print(one_year, df, year)
    one_year = one_year.sort_values(by='total_eth', ascending=False)
    top_table_src = one_year[0:10].to_html()
    return render_template('second.html', years=years, year=year, top_table=top_table_src)


if __name__ == '__main__':
    if not os.path.exists('static/images'):
        os.makedirs('static/images')

    try:
        app.run(debug=True)
    except Exception as e:
        print(f"Flask app failed to run: {e}")
