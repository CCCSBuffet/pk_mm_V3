from matplotlib import pyplot as plt
import numpy as np

def Counts(o):
	if not o['do_counts']:
		return

	''' This function builds the counts data structure and then emits
		the information either in text or in graphical form depending
		on command line options.
		
		No header is printed if the quiet option was specified.
	'''

	if 'counts' not in o.keys():
		# Ensure this is not done twice.
		__GatherAllCounts(o)
	
	if not o['graph']:
		if not o['quiet']:
			print('{:18s}{:25s}{:20s}'.format(' ', 'Majors', 'Minors'))
			print('{:4} {:<13s}'.format('Year', 'Month'), end='')
			print('{:5}{:5}{:5}{:5}{:5}'.format('FF', 'SO', 'JR', 'SR', 'TO'), end='')
			print('{:5}{:5}{:5}{:5}{:5}'.format('FF', 'SO', 'JR', 'SR', 'TO'), end='')
			print('{:5s}'.format('Pct F'))
		for c in o['counts']:
			print('{:4} {:<10s}'.format(c[0], __Month(c[2])), end='')
			__PrintMajorMinor(c, 3)
			__PrintMajorMinor(c, 4)
			sum = c[5][0] + c[5][1]
			if sum != 0:
				print('   {:5.2f}'.format(c[5][0] / sum * 100))
			else:
				print('   N/A')
	else:
		__MakeCohortSizePicture(o)

def __Month(m) -> str:
	months = [None,
		'January',
		'February',
		'March',
		'April',
		'May',
		'June',
		'July',
		'August',
		'September',
		'October',
		'November',
		'December'
	]
	return months[m]


def __ApplyLine(row, r):
	academic_level = row['Classification Code'].strip()
	if academic_level in ['FR', 'UT', 'PF', 'ND', 'FN']:
		academic_level = 'FF'
	if academic_level == 'GD':
		academic_level = 'SR'
	if academic_level not in r:
		r[academic_level] = 0
	r[academic_level] += 1


def __GetGender(row):
	if 'Gender Code' in row.keys():
		if row['Gender Code'] == 'F':
			return 0
		elif row['Gender Code'] == 'M':
			return 1
	return 2

def __GatherCounts(counts, o, year, term, month):
	results = [year, term, month, {}, {}, [0, 0, 0]]
	data = o['student_data'][year][term][month]
	for row in data:
		email = row['Carthage E-mail'].strip()
		if o['major'] in [row['Major 1 Description'].strip(), row['Major 2 Description'].strip()]:
			__ApplyLine(row, results[3])
		if o['minor'] in [
			row['Minor 1 Description'].strip(), 
			row['Minor 2 Description'].strip(),
			row['Minor 3 Description'].strip()
        ]:
			__ApplyLine(row, results[4])
		results[5][__GetGender(row)] += 1

	counts.append(results)

def __GatherAllCounts(o):
	'''	__GatherAllCounts() builds a data structure containing the data used
		in the counts report. The data structure can be formatted for output
		either in text or graphical form. This represents a big step forward
		in design of the tool's internals.
	'''
	s = 'student_data'
	counts = []
	years = list(o[s].keys())
	years.sort()
	terms = ['j-term', 'spring', 'summer', 'fall']
	for year in years:
		for term in terms:
			if term in o[s][year].keys():
				for month in o[s][year][term].keys():
					__GatherCounts(counts, o, year, term, month)
	o['counts'] = counts


def __PrintMajorMinor(c, index):
	academic_levels = ['FF', 'SO', 'JR', 'SR']
	sum = 0
	for al in academic_levels:
		if al in c[index].keys():
			sum += c[index][al]
			print('{:5}'.format(c[index][al]), end='')
		else:
			print('{:>5}'.format('N/A'), end='')
	print('{:>5}'.format(sum if sum > 0 else 'N/A'), end='')


# plt.plot(x_axis, y_axis, label=str(current_year), marker='o')

'''	rows here will never spread across two calendar years the way that
	terms are defined. This will help us handle missing months. When a
	month is detected that is missing, supply a row with None data where
	it counts.
'''

def __GetRows(data, m) -> list:
	rows = { }
	for row in data:
		if row[0] not in rows.keys():
			rows[row[0]] = [ ]
		if row[2] in m:
			# It is possible the row being added is empty
			# except for year and month. This happens  if
			# a month's file was missing.
			rows[row[0]].append(row)
	return rows

def __GetTotal(d) -> int:
	if d == None:
		return 0
	sum = 0;
	for c in d.values():
		sum += c if c != None else 0
	return sum

def __MakeAxes(c, ax, term):
	ax.set_title(term)
	if term == 'Fall':
		months = [9, 10, 11, 12]
	elif term == 'J-Term':
		months = [ 1 ]
	elif term == 'Summer':
		months = [6, 7, 8]
	else:
		months = [2, 3, 4, 5]
	month_names = [ ]
	for m in months:
		month_names.append(__Month(m))
	rows = __GetRows(c, months)
	years = list(rows.keys())
	years.sort()
	for year in years:
		x_axis = list(range(len(months)))
		y_axis = []
		for row in rows[year]:
			if len(row[3]) == 0:
				y_axis.append(None)
			else:
				y_axis.append(__GetTotal(row[3]))
		if len(x_axis) == len(y_axis):
			ax.plot(x_axis, y_axis, label=str(year), marker='o')
		else:
			pass
			#print(year, term, x_axis, y_axis)
	ax.set_xticks(x_axis)
	ax.set_xticklabels(month_names)
	ax.legend()

def __MakeCohortSizePicture(o):
	if 'counts' not in o.keys():
		print('o does not contain key: counts - please report this')
		return
		
	fig, ax = plt.subplots(2, 2, figsize=(12, 8))
	x_axis = list(range(10))
	y_axis = list(range(10))

	if len(o['counts']) != 0:
		__MakeAxes(o['counts'], ax[0][0], 'Fall')
		__MakeAxes(o['counts'], ax[0][1], 'Spring')
		__MakeAxes(o['counts'], ax[1][0], 'J-Term')
		__MakeAxes(o['counts'], ax[1][1], 'Summer')
		plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.4)
		plt.suptitle(o['major'] + ' - Size of Major Year over Year')
		#plt.show()
		file_name = "majors_total_yoy.png"
		plt.savefig(file_name)
		print('Cohort Sizes by Month image saved with file name:', file_name)

	else:
		print("o['counts'] contains no data - please report this")

def Breakdown(o):
	if not o['do_breakdown']:
		return
	if 'counts' not in o.keys():
		# Ensure this is not done twice.
		__GatherAllCounts(o)
	covered_terms = __BuildSetOfCoveredYearsAndTerms(o['counts'])
	data = [ ]
	for term in covered_terms:
		data.append((term, __ComputeAverages(term, o['counts'])))
	# data looks like this:
	# ((2018, 'j-term'), {'FF': 27.0, 'SO': 8.0, 'JR': 21.0, 'SR': 19.0})
	if not o['graph']:
		if not o['quiet']:
			print('{:4s} {:<8s} {:>6s} {:>6s} {:>6s} {:>6s} '.format(
				'Year', 'Term', 'FF', 'SO', 'JR', 'SR'))
		for d in data:
			if o['term'] != '' and d[0][1] != o['term']:
				continue
			print('{:4} {:<8s} '.format(d[0][0], d[0][1]), end='')
			print('{:>6.0f} {:>6.0f} '.format(d[1]['FF'], d[1]['SO']), end='')
			print('{:>6.0f} {:>6.0f}'.format(d[1]['JR'], d[1]['SR']))
	else:
		__MakeBreakDownChart(o, data)

def __MakeBreakDownChart(o, data):
	# data looks like this:
	# ((2018, 'j-term'), {'FF': 27.0, 'SO': 8.0, 'JR': 21.0, 'SR': 19.0})
	fig, ax = plt.subplots()
	al = ['FF', 'SO', 'JR', 'SR']
	count = len(data)
	labels = [ ]
	y_axes = { }
	npy = [ ]

	for l in al:
		y_axes[l] = []
	for d in data:
		if o['term'] != '' and d[0][1] != o['term']:
			continue
		labels.append(d[0][1] + ' ' + str(d[0][0]))
		for index, l in enumerate(al):
			y_axes[l].append(d[1][l])
	npy = np.zeros(len(labels))
	for k in al:
		ax.bar(labels, y_axes[k], bottom=npy, label=k)
		npy = npy + np.array(y_axes[k])

	plt.suptitle(o['major'] + ' - Distribution of Academic Levels by Term')
	fig.autofmt_xdate(rotation=45)
	fig.subplots_adjust(bottom=0.2)
	ax.legend()
	file_name = "cohorts_by_term.png"
	plt.savefig(file_name)
	print('Cohorts by Term image saved with file name:', file_name)

def __BuildSetOfCoveredYearsAndTerms(counts):
	t = [ ]
	for year in counts:
		tuple = (year[0], year[1])
		if tuple not in t:
			t.append(tuple)
	return t

# [2022, 'summer', 6, {'JR': 23, 'SR': 16, 'SO': 19, 'FF': 48}, {'SR': 5, 'SO': 6, 'FF': 11, 'JR': 3}, [27, 104, 0]]

def __AreCountsMissing(s) -> bool:
	results = False
	for v in s.values():
		if v > 0:
			results = True
			break
	return results

def __ComputeAverages(t, c):
	year = t[0]
	term = t[1]
	sums = { 'FF': 0, 'SO': 0, 'JR' : 0, 'SR': 0}
	averages = {'FF': 0, 'SO': 0, 'JR': 0, 'SR': 0}
	counter = 0
	for row in c:
		if row[0] != year or row[1] != term:
			continue
		if not __AreCountsMissing(row[3]):
			continue
		for k in row[3].keys():
			sums[k] += row[3][k]
		counter += 1
	for k in averages.keys():
		averages[k] = sums[k] / counter
	return averages