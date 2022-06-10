# coding: utf-8
"""
Author: 姚惠馨
Github: https://github.com/Hsin0705
Date: 2022.06.06
"""

from influxdb import InfluxDBClient
import dash
from dash import dcc
from dash import html
import plotly_express as px
import pandas as pd
import plotly.graph_objects as go

client = InfluxDBClient('54.180.25.155',8086,'','','stock_data')

app = dash.Dash(__name__)

app.layout = html.Div([
     
    dcc.Graph(id = 'fig'),
    dcc.Graph(id = 'fig2'),
    
    dcc.Interval(
        id='interval-component',
        interval=5*1000,
        n_intervals=0
    )
])

@app.callback(
    dash.dependencies.Output("fig", "figure"), 
    dash.dependencies.Output("fig2", "figure"), 
    [dash.dependencies.Input('interval-component', 'n_intervals')])

def update(n):
    
    result = client.query('select * from web_crawler_data')
    result2 = client.query('select * from prediction_data')

    data = pd.DataFrame(list(result.get_points()))['value'].str.split(expand=True)
    data.columns = ['amount', 'average_price', 'buy_price', 'buy_volume', 'change_price', 'change_rate', 'close', 'high', 'low', 'open', 'sell_price', 'sell_volume', 'total_amount', 'total_volume', 'volume', 'volume_ratio', 'yesterday_volume', 'date', 'time', 'stock_id', 'TickType']
    df=pd.DataFrame([])
    df['close'] = pd.to_numeric(data['close'])
    df['time'] = data['time']
    df['H'] = pd.to_numeric(df['time'].str[0:2])
    df['M'] = pd.to_numeric(df['time'].str[3:5])
    df['S'] = pd.to_numeric(df['time'].str[6:8])
    df['id'] = (((df['H']-9)*60+df['M'])*60+df['S'])/3600
    df = df.append({'id':0}, ignore_index=True)
    df = df.append({'id':4.5}, ignore_index=True)

    fig = go.Figure(go.Scatter(x=df['id'], y=df['close'],
                        mode='lines',
                        name='lines',
                        line=dict(color='black', width=1)))

    fig.update_layout(
        xaxis = dict(
            tickmode = 'array',
            tickvals = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5],
            ticktext = ['9:00', '9:30', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00', '13:30']
        ),
        title = '2330'
    )
    fig.update_yaxes(title_text = '股價')
    ############################################################################################################

    data2 = pd.DataFrame(list(result2.get_points()))['value'].str.split(expand=True)
    data2.columns = ['amount', 'average_price', 'buy_price', 'buy_volume', 'change_price', 'change_rate', 'close', 'high', 'low', 'open', 'sell_price', 'sell_volume', 'total_amount', 'total_volume', 'volume', 'volume_ratio', 'yesterday_volume', 'date', 'time', 'stock_id', 'TickType']
    df2=pd.DataFrame([])
    df2['close'] = pd.to_numeric(data2['close'])
    df2['time'] = data2['time']
    df2['H'] = pd.to_numeric(df2['time'].str[0:2])
    df2['M'] = pd.to_numeric(df2['time'].str[3:5])
    df2['S'] = pd.to_numeric(df2['time'].str[6:8])
    df2['id'] = (((df2['H']-9)*60+df2['M'])*60+df2['S'])/3600
    df2 = df2.append({'id':0}, ignore_index=True)
    df2 = df2.append({'id':4.5}, ignore_index=True)

    fig2 = go.Figure(go.Scatter(x=df2['id'], y=df2['close'],
                        mode='lines',
                        name='lines',
                        line=dict(color='blue', width=1)))

    fig2.update_layout(
        xaxis = dict(
            tickmode = 'array',
            tickvals = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5],
            ticktext = ['9:00', '9:30', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00', '13:30']
        )
    )
    fig2.update_yaxes(title_text = '股價')
    
    return fig, fig2


if __name__ == "__main__":
    app.run_server(debug=True)