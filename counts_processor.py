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


# [2022, 'summer', 6, {'JR': 23, 'SR': 16, 'SO': 19, 'FF': 48}, {'SR': 5, 'SO': 6, 'FF': 11, 'JR': 3}, [27, 104, 0]]

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
	__GatherAllCounts(o)
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
