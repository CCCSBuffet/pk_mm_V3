import data_reader
from matplotlib import pyplot as plt

def MajorPairings(o):
    if not o['do_Pairings']:
        return
    pairings = __CollectMajors(o)
    if not o['graph']:
        if not o['quiet']:
            print('{:<24} {:<24} {:<6}'.format('Major 1', 'Major 2', 'Count'))
        l = list(pairings.keys())
        l.sort()
        for key in l:
            print('{:<24} '.format(key[0]), end='')
            print('{:<24} '.format(key[1]), end='')
            print('{:<6}'.format(pairings[key]))
    else:
        __MakeMajorChart(o, pairings)
        
def MinorPairings(o):
    if not o['do_pairings']:
        return
    pairings, counts = __CollectMinors(o)
    if not o['graph']:
        if not o['quiet']:
            print('{:<24} {:<24} {:<6}'.format('Major', 'Minor', 'Count'))
        l = list(pairings.keys())
        l.sort()
        for key in l:
            print('{:<24} '.format(key[0]), end='')
            print('{:<24} '.format(key[1]), end='')
            print('{:<6}'.format(pairings[key]))
        print()
        print('{:<24s}{:5}'.format('Majors with no minors', counts[0]))
        print('{:<24s}{:5}'.format('Majors with one minors', counts[1]))
        print('{:<24s}{:5}'.format('Majors with two minors', counts[2]))
        print('{:<24s}{:5}'.format('Majors with three minors', counts[3]))

def __CollectMajors(o) -> dict:
    pairings = {}
    major = o['major']
    month = int(o['end_month'][-6:-4])
    term = data_reader.DetermineTerm(month)
    year  = int(int(o['end_month'][-11: -7]))
    d = o['student_data'][year][term][month]
    for row in d:
        M1 = row['Major 1 Description'].strip()
        M2 = row['Major 2 Description'].strip()
        if M1 != major and M2 != major:
            continue
        M = (M2, M1) if M2 == major else (M1, M2)
        if M not in pairings.keys():
            pairings[M] = 0
        pairings[M] += 1
    return pairings

def __CollectMinors(o) -> dict:
    pairings = {}
    counts = [ 0, 0, 0, 0]
    major = o['major']
    month = int(o['end_month'][-6:-4])
    term = data_reader.DetermineTerm(month)
    year  = int(int(o['end_month'][-11: -7]))
    pairings[(major,'')] = 0
    d = o['student_data'][year][term][month]
    for row in d:
        M1 = row['Major 1 Description'].strip()
        M2 = row['Major 2 Description'].strip()
        if M1 != major and M2 != major:
            # this person is not a major
            continue
        M1 = M1 if M1 == major else M2
        flag = False
        minors = [
            row['Minor 1 Description'].strip(),
            row['Minor 2 Description'].strip(),
            row['Minor 3 Description'].strip()
        ]
        count = 0
        for m in minors:
            if m == '':
                # if the minor is empty, skip it to avoid double counting
                continue 
            M = (M1, m)
            if M not in pairings.keys():
                pairings[M] = 0
            pairings[M] += 1
            flag = True
            count += 1
        if not flag:
            pairings[(major,'')] += 1
        counts[count] += 1
    return pairings, counts


def __MakeMajorChart(o, pairings):
    pass


'''
# Pie chart, where the slices will be ordered and plotted counter-clockwise:
labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
sizes = [15, 30, 45, 10]
explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.show()
'''