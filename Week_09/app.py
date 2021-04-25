import dash
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import base64
import pyreadr


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__,external_stylesheets=external_stylesheets)



# -------------------------------------------------------------------------------------------------------------- 

#											PART 1: DESIGN PARAMETERS

# --------------------------------------------------------------------------------------------------------------
# Here we will set the colors, margins, DIV height&weight and other parameters

colors = {
		'full-background': 	'#DCDCDC',
		'block-borders': 	'#202020'
}

margins = {
		'block-margins': '5px 5px 5px 5px'
}

sizes = {
		'subblock-heights': '380px'
}



# -------------------------------------------------------------------------------------------------------------- 

#											PART 2: ACTUAL LAYOUT

# --------------------------------------------------------------------------------------------------------------
# Here we will set the DIV-s and other parts of our layout
# We need too have a 2x2 grid
# I have also included 1 more grid on top of others, where we will show the title of the app



# -------------------------------------------------------------------------------------- DIV for TITLE
div_title = html.Div(children =	html.H1('Title', style=	{'color': 'blue', 'margin-left': -40}),
					style ={
							'border': '3px {} solid'.format(colors['block-borders']),
							'margin': margins['block-margins'],
							'text-align': 'center'
							}
					)

# -------------------------------------------------------------------------------------- DIV for first raw (1.1 and 1.2)

chess_img = 'Chess_Winners.png'
chess_base64 = base64.b64encode(open(chess_img, 'rb').read()).decode('ascii')

div_1_1 = html.Img(src='data:image/png;base64,{}'.format(chess_base64),
					style = {
							'border': '1px {} solid'.format(colors['block-borders']),
							'margin':  margins['block-margins'],
							'width': '49%',
							'height': sizes['subblock-heights'],
					}
				)


dist_img = 'Dist.png'
dist_base64 = base64.b64encode(open(dist_img, 'rb').read()).decode('ascii')

div_1_2 = html.Img(src='data:image/png;base64,{}'.format(dist_base64),
					style = {
							'border': '1px {} solid'.format(colors['block-borders']),
							'margin': margins['block-margins'],
							'width': '51%',
							'height': sizes['subblock-heights']
					}
				)

# Collecting DIV 1.1 and 1.2 into the DIV of first raw.
# Pay attention to the 'display' and 'flex-flaw' attributes.
# With this configuration you are able to let the DIV-s 1.1 and 1.2 be side-by-side to each other.
# If you skip them, the DIV-s 1.1 and 1.2 will be ordered as separate rows.
# Pay also attention to the 'width' attributes, which specifiy what percentage of full row will each DIV cover.
div_raw1 = html.Div(children =	[div_1_1,
								div_1_2
								],
					style ={
							'border': '3px {} solid'.format(colors['block-borders']),
							'margin': margins['block-margins'],
							'display': 'flex',
							'flex-flaw': 'row-wrap'
							})


# -------------------------------------------------------------------------------------- DIV for second raw (2.1 and 2.2)

df = pyreadr.read_r("f_data_sm.rda")["f_data_sm"]
df = df.rename(columns={'FTSC': 'SCORE',
                   'FTR': 'WON',
                   'FTHG': 'HOME_GOALS',
                   'FTAG': 'AWAY_GOALS',
                   'FTTG': 'TOTAL_GOALS'})
df = df.drop(['H', 'D', 'A'], axis = 1)
df = df.dropna()
df = df.astype({'SEASON': 'int',
          'HOME_GOALS': 'int',
          'AWAY_GOALS': 'int',
          'TOTAL_GOALS': 'int'})

la_liga = df[df["COUNTRY"] == "Spain"]

home_mean_goals = la_liga.groupby(['HOMETEAM', 'SEASON'], as_index= False).agg({'HOME_GOALS': 'mean'})
home_mean_goals = home_mean_goals.rename(columns = {'HOME_GOALS': 'HOME_MEAN', 'HOMETEAM': 'TEAM'})

away_mean_goals = la_liga.groupby(['AWAYTEAM', 'SEASON'], as_index= False).agg({'AWAY_GOALS': 'mean'})
away_mean_goals = away_mean_goals.rename(columns = {'AWAY_GOALS': 'AWAY_MEAN', 'AWAYTEAM': 'TEAM'})

concat_1 = home_mean_goals.set_index(['TEAM', 'SEASON'])
concat_2 = away_mean_goals.set_index(['TEAM', 'SEASON'])
plot_data = pd.concat([concat_1, concat_2], axis = 1).reset_index()

Barca = plot_data[plot_data['TEAM'] == 'Barcelona']
Real_Madrid = plot_data[plot_data['TEAM'] == 'Real Madrid']

div_fig_Barca = go.Figure()
div_fig_Barca.add_trace(go.Scatter(x = Barca['SEASON'], y = Barca['HOME_MEAN'],
                                  name = "Mean home goals"))
div_fig_Barca.add_trace(go.Scatter(x = Barca['SEASON'], y = Barca['AWAY_MEAN'],
                                  name = "Mean away goals"))
div_fig_Barca.update_layout(title={'text': "Barçelona", 'x':0.42})
div_fig_Barca.update_layout(legend=dict(orientation="h",
	yanchor="bottom", xanchor="right", x = 1, y = 1))

div_fig_Real = go.Figure()
div_fig_Real.add_trace(go.Scatter(x = Real_Madrid['SEASON'], y = Real_Madrid['HOME_MEAN'],
                                  name = "Mean home goals"))
div_fig_Real.add_trace(go.Scatter(x = Real_Madrid['SEASON'], y = Real_Madrid['AWAY_MEAN'],
                                  name = "Mean away goals"))
div_fig_Real.update_layout(title={'text': "Real Madrid", 'x':0.42})
div_fig_Real.update_layout(legend=dict(orientation="h",
	yanchor="bottom", xanchor="right", x = 1, y = 1))

div_2_1 = dcc.Graph (id = 'Barcelona',
					figure = div_fig_Barca,
					style = {
							'border': '1px {} solid'.format(colors['block-borders']),
							'margin': margins['block-margins'],
							'width': '49%',
							'height': sizes['subblock-heights'],
					}
				)

div_2_2 = dcc.Graph (id = 'Real Madrid',
					figure = div_fig_Real,
					style = {
							'border': '1px {} solid'.format(colors['block-borders']),
							'margin': margins['block-margins'],
							'width': '51%',
							'height': sizes['subblock-heights'],
					}
				)


div_raw2 = html.Div(children =	[div_2_1,
								div_2_2
								],
					style ={
							'border': '3px {} solid'.format(colors['block-borders']),
							'margin': margins['block-margins'],
							'display': 'flex',
							'flex-flaw': 'row-wrap'
							})

# -------------------------------------------------------------------------------------- Collecting all DIV-s in the final layout
# Here we collect all DIV-s into a final layout DIV

app.layout = html.Div(	[
						div_title,
						div_raw1,
						div_raw2
						],
						style = {
							'backgroundColor': colors['full-background']
						}
					)




# -------------------------------------------------------------------------------------------------------------- 

#											PART 3: RUNNING THE APP

# --------------------------------------------------------------------------------------------------------------
# >> use __ debug=True __ in order to be able to see the changes after refreshing the browser tab,
#			 don't forget to save this file before refreshing
# >> use __ port = 8081 __ or other number to be able to run several apps simultaneously
app.run_server(debug=True, port = 8081)