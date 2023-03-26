# -*- coding: utf-8 -*-

from dash import Dash, dcc, html
import pandas as pd
from dash.dependencies import Input, Output
from datetime import datetime, time
import plotly.graph_objs as go


#charger le fichier CSV à partir de l'instance AWS
lvmh_data = pd.read_csv('/home/ec2-user/Project/WebScrappingBensimonIris/cours_action.csv', names = ['Date','Price'])

# fonction pour calculer le rendement journalier
def daily_return(df):
	return ((df.iloc[-1]['Price'] - df.iloc[0]['Price']) / df.iloc[0]['Price']) * 100

# fonction pour calculer la volatilité journalière
def daily_volatility(df):
	return df['Price'].pct_change().std() * 100


# initialiser l'application Dash
app = Dash(__name__)

fig = go.Scatter(
	x=lvmh_data['Date'],
	y=lvmh_data['Price'],
	mode='lines',
	name='LVMH'
)


# créer le layout du dashboard
app.layout = html.Div([html.H1('Dashboard LVMH'),

	# graphique avec les prix de l'action
	dcc.Graph(id='price-graph',
		figure={
		'data':[fig],
		'layout': go.Layout(
			xaxis={'title': 'Date'},
			yaxis={'title': 'Price'}
		)
	}),



	# dropdown pour choisir la période de temps
	html.Label('Période de temps'),
	dcc.Dropdown(
		id='time-period',
		options=[
			{'label': '5 minutes', 'value': '5min'},
			{'label': '30 minutes', 'value': '30min'},
			{'label': '1 heure', 'value': '1h'},
			{'label': 'all', 'value': 'all'}
		],
		value='all'
	),

# tableau avec les informations sur les prix
	html.H2('Informations sur les prix'),
	html.Table([
		html.Tr([html.Th('Prix d\'ouverture'), html.Td(id='open-price')]),
		html.Tr([html.Th('Prix de fermeture'), html.Td(id='close-price')]),
		html.Tr([html.Th('Volatilité journalière'), html.Td(id='daily-volatility')]),
		html.Tr([html.Th('Rendement journalier'), html.Td(id='daily-return')])
	])
])

# callback pour mettre à jour le graphique en fonction de la période de temps choisie
@app.callback(Output('price-graph', 'figure'),Input('time-period', 'value'))

def update_graph(time_period):
    # récupérer les données correspondant à la période de temps choisie
	if time_period == '5min':
		df = lvmh_data.tail(60)
	elif time_period == '30min':
		df = lvmh_data.tail(360)
	elif time_period == '1h':
		df = lvmh_data.tail(720)
	else:
		df = lvmh_data.tail(len(lvmh_data))

    # créer le graphique avec Plotly
	fig = {'data': [{'x': df['Date'], 'y': df['Price'], 'type': 'line'}],'layout': {'title': 'Prix de l\'action LVMH'}}

	return fig


@app.callback(Output('open-price', 'children'),
              Output('close-price', 'children'),
              Output('daily-volatility', 'children'),
              Output('daily-return', 'children'),
              Input('interval-component', 'n_intervals'))


# fonction pour calculer les metrics
def update_info(n):
    # récupérer les données correspondant à la journée
        today = datetime.today()
        nine_am = time(hour=9, minute=0, second=0)
        today_at_nine = datetime.combine(today, nine_am)

        five_pm = time(hour=17, minute=30, second=0)
        today_at_five = datetime.combine(today, five_pm)

        today_data = lvmh_data.loc[(lvmh_data['Date'] >= today_at_nine) & (lvmh_data['Date'] <= today_at_five)]

    # calculer les informations sur les prix
        open_price = today_data.iloc[0]['Price']
        close_price = today_data.iloc[-1]['Price']
        daily_vol = daily_volatility(today_data)
        daily_ret = daily_return(today_data)

    # retourner les informations sous forme de chaînes de caractères
        return '{:.2f} €'.format(open_price), '{:.2f} €'.format(close_price), '{:.2f}%'.format(daily_vol), '{:.2f}%'.format(daily_ret)
  


if __name__ == '__main__':
	app.run_server(host = "0.0.0.0",port = 8050, debug=True)

