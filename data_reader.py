from calendar import month
import os
import sys
import csv

def ReadData(o) -> bool:
	starting_month_found = False

	for f in o['files']:
		if not starting_month_found and f != o['start_month']:
			continue
		starting_month_found = True
		__ProcessFile(o, f)
		if f == o['end_month']:
			break
	return True

def __DetermineTerm(mo) -> str:
	if (mo == 1):
		return 'j-term'
	if (mo >= 2 and mo <= 5):
		return 'spring'
	if (mo >= 9 and mo <= 12):
		return 'fall'
	return 'summer'

def __ProcessFile(o, f):
	f = os.path.join(o['folder'], f)
	month = int(f[-6:-4])
	term = __DetermineTerm(month)
	year = int(f[-11: -7])
	if 'student_data' not in o.keys():
		o['student_data'] = { }
	if year not in o['student_data'].keys():
		o['student_data'][year] = { }
	if term not in o['student_data'][year].keys():
		o['student_data'][year][term] = {}
	o['student_data'][year][term][month] = []
	###
	with open(f, 'r') as file:
		reader = csv.DictReader(file)
		for line in reader:
			o['student_data'][year][term][month].append(line)
