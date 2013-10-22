'''
state_cvs_parser.py reads in the state CSV files into dictionaries.

@author Ben Zoller
'''

import csv
from state import State
from state_districts import StateDistricts

def read_states_csv():
	file = open('csv/states.csv', 'r')
	reader = csv.reader(file)
	states = {}
	for row in reader:
		abbrev = row[0]
		name = row[1]
		states[abbrev] = State(name, abbrev)
	file.close()
	return states

def read_state_districts_csv(states, year):
	filepath = "csv/{}.csv".format(year)
	file = open(filepath, 'r')
	reader = csv.reader(file)
	state_districts = {}
	for row in reader:
		abbrev = row[0]
		districts = int(row[1])
		state = states[abbrev]
		state_districts[abbrev] = StateDistricts(state, districts)
	file.close()
	return state_districts


def get_total_num_districts(state_districts):
	total = 0
	for state_district in state_districts.values():
		total += state_district.districts
	return total	

if __name__ == "__main__":
	states = read_states_csv()
	districts_2000 = read_state_districts_csv(states, 2000)
	districts_2010 = read_state_districts_csv(states, 2010)

	total_districts_2000 = get_total_num_districts(districts_2000)
	total_districts_2010 = get_total_num_districts(districts_2010)
	print("2000={}; 2010={}".format(total_districts_2000, 
		total_districts_2010))
