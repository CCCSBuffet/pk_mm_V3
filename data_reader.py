from calendar import month
import os
import sys
import csv

def ReadData(o) -> bool:
	starting_month_found = False

	for f in o['files']:
		if not starting_month_found and f != o['start_month']:
			continue
		month = int(f[-6:-4])
		year  = int(int(f[-11: -7]))
		if not starting_month_found:
			month_ordinal = month
			starting_month_found = True
		if month > month_ordinal:
			for m in range(month_ordinal, month):
				__ProcessMissingFile(o, m, year)
				print(year, m, 'was missing', file=sys.stderr)
			month_ordinal += 1
		#print(year, month, f, 'processed')
		__ProcessFile(o, f)
		month_ordinal = month + 1
		if month_ordinal == 13:
			month_ordinal = 1
			year += 1
		if f == o['end_month']:
			break
	return True

def DetermineTerm(mo) -> str:
	if (mo == 1):
		return 'j-term'
	if (mo >= 2 and mo <= 5):
		return 'spring'
	if (mo >= 9 and mo <= 12):
		return 'fall'
	return 'summer'

def __MakeMonth(o, month, year, term):
	if 'student_data' not in o.keys():
		o['student_data'] = {}
	if year not in o['student_data'].keys():
		o['student_data'][year] = {}
	if term not in o['student_data'][year].keys():
		o['student_data'][year][term] = {}
	o['student_data'][year][term][month] = []

def __ProcessFile(o, f):
	if f == None:
		print('missing file')
		return
	f = os.path.join(o['folder'], f)
	month = int(f[-6:-4])
	term = DetermineTerm(month)
	year = int(f[-11: -7])
	__MakeMonth(o, month, year, term)
	with open(f, 'r') as file:
		reader = csv.DictReader(file)
		for line in reader:
			o['student_data'][year][term][month].append(line)


def __ProcessMissingFile(o, month, year):
	term = DetermineTerm(month)
	__MakeMonth(o, month, year, term)
