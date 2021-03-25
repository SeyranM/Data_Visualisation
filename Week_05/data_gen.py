import sqlite3
import numpy as np
import time
from scipy import stats

connection = sqlite3.connect('data_db.db')
c = connection.cursor()

c.execute("DROP TABLE IF EXISTS dices")
c.execute("DROP TABLE IF EXISTS means")
c.execute("DROP TABLE IF EXISTS shw_p_values")
c.execute("DROP TABLE IF EXISTS jb_p_values")

c.execute("CREATE TABLE dices (ID int, dices int)")
c.execute("CREATE TABLE means (ID int, means float)")
c.execute("CREATE TABLE shw_p_values (ID int, shw_p_values float)")
c.execute("CREATE TABLE jb_p_values (ID int, jb_p_values float)")

iteration = 0
throws = []
mean_values = []
p_vals = []
jb_p_vals = []

while True:
	throw_result = np.random.randint(1, 7, 7)
	for i in throw_result:
		throws.append(i)
	mean_values.append(np.mean(throw_result))
	if len(mean_values) >= 3:
		p_vals.append(stats.shapiro(mean_values)[1])
		jb_p_vals.append(stats.jarque_bera(mean_values)[1])
		c.execute("INSERT INTO shw_p_values values ({},{})".format(iteration, p_vals[-1]))
		c.execute("INSERT INTO jb_p_values values ({},{})".format(iteration, jb_p_vals[-1]))
	for i in range(iteration * 7, (iteration * 7) + 7):
		c.execute("INSERT INTO dices values ({},{})".format(i + 1, throws[i]))
	c.execute("INSERT INTO means values ({},{})".format(iteration + 1, mean_values[-1]))
	connection.commit()
	iteration += 1
	time.sleep(0.5)