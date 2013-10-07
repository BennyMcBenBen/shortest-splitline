'''
StateCsvParser reads in the state CSV files into dictionaries.
@author Ben Zoller
'''

import csv
from state import State

def read_states_csv():
	file = open('csv/states.csv', 'r')
	reader = csv.reader(file)
	states = {}
	for row in reader:
		abbrev = row[0]
		name = row[1]
		states[abbrev] = State(name, abbrev)
	return states

states = read_states_csv()
print(states)
