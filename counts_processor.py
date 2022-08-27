from matplotlib import pyplot as plt

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
	if not o['do_counts']:
		return

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
			print('{:5}'.format('NA'), end='')
	print('{:5}'.format(sum), end='')

def Counts(o):
	''' This function builds the counts data structure and then emits
		the information either in text or in graphical form depending
		on command line options.
		
		No header is printed if the quiet option was specified.
	'''
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
			print('   {:5.2f}'.format(c[5][0] / (c[5][0] + c[5][1]) * 100))
	else:
		__MakePicture(o)

# plt.plot(x_axis, y_axis, label=str(current_year), marker='o')
# [2022, 'summer', 6, {'JR': 23, 'SR': 16, 'SO': 19, 'FF': 48}, {'SR': 5, 'SO': 6, 'FF': 11, 'JR': 3}, [27, 104, 0]]

def __GetRows(data, m) -> list:
	rows = { }
	for row in data:
		if row[2] in m:
			if not row[0] in rows.keys():
				rows[row[0]] = [ ]
			rows[row[0]].append(row)
	return rows

def __GetTotal(d) -> int:
	sum = 0;
	for c in d.values():
		sum += c
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
			y_axis.append(__GetTotal(row[3]))
		print(x_axis, y_axis)
		if len(x_axis) == len(y_axis):
			ax.plot(x_axis, y_axis, label=str(year), marker='o')
	ax.set_xticks(x_axis)
	ax.set_xticklabels(month_names)
	ax.legend()
	#print(rows)

def __MakePicture(o):
	fig, ax = plt.subplots(2, 2, figsize=(12, 8))
	x_axis = list(range(10))
	y_axis = list(range(10))

	__MakeAxes(o['counts'], ax[0][0], 'Fall')
	__MakeAxes(o['counts'], ax[0][1], 'Spring')
	__MakeAxes(o['counts'], ax[1][0], 'J-Term')
	__MakeAxes(o['counts'], ax[1][1], 'Summer')
	plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.4)
	plt.suptitle(o['major'])
	plt.show()
