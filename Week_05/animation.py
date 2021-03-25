import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy import stats

import time

import sqlite3
connection = sqlite3.connect('data_db.db')
c = connection.cursor()	

fig = plt.figure()
fig.set_size_inches(17,9)
gs = fig.add_gridspec(2,4)
ax_1 = fig.add_subplot(gs[0,0])
ax_2 = fig.add_subplot(gs[0,1])
ax_3 = fig.add_subplot(gs[1,0])
ax_4 = fig.add_subplot(gs[1,1])
ax_5 = fig.add_subplot(gs[:,2:])

def animate(i):

	ax_1.cla()
	ax_2.cla()
	ax_3.cla()
	ax_4.cla()
	ax_5.cla()
	query_1 = ('SELECT * FROM means')
	data_1 = pd.read_sql_query(query_1, connection)
	x_1 = data_1.means
	ax_1.hist(x_1)
	ax_1.set_title('Distribution of means')

	stats.probplot(x_1, dist='norm', plot=ax_2)

	query_3 = ('SELECT * FROM shw_p_values')
	data_3 = pd.read_sql_query(query_3, connection)
	x_3 = data_3.shw_p_values.values
	ax_3.text(0.33, 0.5, 'p-value: ' + str(np.round(x_3[-1], 4)))
	ax_3.set_axis_off()
	ax_3.set_title('Normality test p-value')

	query_4 = ('SELECT * FROM jb_p_values')
	data_4 = pd.read_sql_query(query_4, connection)
	x_4 = data_4.jb_p_values.values
	ax_4.plot(data_4.ID, x_4)
	ax_4.set_title('Historical p-values')

	query_5 = ('SELECT * FROM dices')
	data_5 = pd.read_sql_query(query_5, connection).dices.value_counts()
	x_5 = np.array(data_5.index)
	y_5 = np.array(data_5.values)
	ax_5.bar(x_5, y_5)



ani = FuncAnimation(plt.gcf(), animate, interval = 500)

plt.show()