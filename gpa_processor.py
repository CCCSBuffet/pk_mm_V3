import data_reader
from matplotlib import pyplot as plt

def __GetCohort(al) -> str:
	if al == 'FF':
		return 'Freshpersons'
	if al == 'SO':
		return 'Sophomores'
	if al == 'JR':
		return 'Juniors'
	return 'Seniors'

def EMAIL(o):
	if o['do_email'] == '' and o['do_EMAIL'] == '':
		return
	data = __CollectEmail(o)
	for d in data:
		print(d)

def GPA(o):
	if o['do_gpa'] == '':
		return
	gpa_limiter = 100
	if o['gpa_lt'] != '':
		gpa_limiter = float(o['gpa_lt'])
	elif o['gpa_ge'] != '':
		gpa_limiter = float(o['gpa_ge'])
	data = __CollectGPA(o)
	for al in data.keys():
		if o['do_gpa'] != 'all' and o['do_gpa'] != al:
			continue
		if not o['quiet']:
			print(__GetCohort(al))
			print('{:<8s}'.format('ID'), end='')
			print('{:<20s}'.format('Last Name'), end='')
			print('{:<20s}'.format('First Name'), end='')
			print('{:<8s}'.format('Gender'), end='')
			print('{:<8s}'.format('GPA'), end='')
			print('{:<16s}'.format('Email'))
		for s in data[al]:
			if  (o['gpa_lt'] != '' and float(s[4]) < gpa_limiter) or \
				(o['gpa_ge'] != '' and float(s[4]) >= gpa_limiter):
				if o['csv']:
					print('{:},'.format(s[0]), end='')
					print('{:},'.format(s[1]), end='')
					print('{:},'.format(s[2]), end='')
					print('{:},'.format(s[3]), end='')
					print('{:},'.format(s[4]), end='')
					if s[5] == 'N/A':
						print(s[5])
					else:
						print('{0}'.format(s[2] + ' ' + s[1] + ' <' + s[5] + '>'))
				else:
					print('{:<8s}'.format(s[0]), end='')
					print('{:<20s}'.format(s[1]), end='')
					print('{:<20s}'.format(s[2]), end='')
					print('{:<8s}'.format(s[3]), end='')
					print('{:<8s}'.format(s[4]), end='')
					if s[5] == 'N/A':
						print(s[5])
					else:
						print('{0}'.format(s[2] + ' ' + s[1] + ' <' + s[5] + '>'))


def __GetAL(row) -> str:
	academic_level = row['Classification Code'].strip()
	if academic_level in ['FR', 'UT', 'PF', 'ND', 'FN']:
		academic_level = 'FF'
	if academic_level == 'GD':
		academic_level = 'SR'
	return academic_level

def __CollectEmail(o):
	discipline = o['major']
	month = int(o['end_month'][-6:-4])
	term = data_reader.DetermineTerm(month)
	year = int(int(o['end_month'][-11: -7]))
	d = o['student_data'][year][term][month]
	data = []
	for row in d:
		M1 = row['Major 1 Description'].strip()
		M2 = row['Major 2 Description'].strip()
		m1 = row['Minor 1 Description'].strip()
		m2 = row['Minor 2 Description'].strip()
		m3 = row['Minor 3 Description'].strip()
		if (o['do_EMAIL'] and (M1 == discipline or M2 == discipline)) or \
		   (o['do_email'] and (m1 == discipline or m2 == discipline or m2 == discipline)):
			data.append(row['Carthage E-mail'].strip())
	return data

def __CollectGPA(o):
	gpa = {
		'FF': [],
		'SO': [],
		'JR': [],
		'SR': []
	}

	major = o['major']
	month = int(o['end_month'][-6:-4])
	term = data_reader.DetermineTerm(month)
	year = int(int(o['end_month'][-11: -7]))
	d = o['student_data'][year][term][month]
	for row in d:
		M1 = row['Major 1 Description'].strip()
		M2 = row['Major 2 Description'].strip()
		if M1 != major and M2 != major:
			continue
		if '\ufeffStudent ID Number' in row.keys():
			id_number = row['\ufeffStudent ID Number']
		else:
			id_number = row['Student ID Number']
		cohort = __GetAL(row)
		if o['do_gpa'] == 'all' or o['do_gpa'] == cohort:
			gpa[__GetAL(row)].append([
				id_number,
				row['Last Name'].strip(),
				row['First Name'].strip(),
				row['Gender Code'] if 'Gender Code' in row.keys() else '-',
				row['Cumulative GPA'].strip(),
				row['Carthage E-mail'].strip() 
					if 'Carthage E-mail' in row.keys() else "N/A"
			])
	#print(gpa)
	return gpa

