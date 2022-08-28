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
        __MakeMajorChart(o, 
            pairings, 
            'double_majors.png',
            'No Double Major',
            'Double Majors'
        )
        
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
    else:
        __MakeMajorChart(o, 
            pairings, 
            'minors.png',
            'No Minor',
            'Minors'
        )

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


def __MakeMajorChart(o, pairings, file_name, no_text, t):
    labels = []
    minors = []
    values = []
    month = int(o['end_month'][-6:-4])
    year = int(int(o['end_month'][-11: -7]))

    l = list(pairings.keys())
    l.sort()
    total = 0
    for key in l:
        minors.append(key[1] if key[1] != '' else no_text)
        values.append(pairings[key])
        total += pairings[key]
    percentage = [ pairings[key] * 100.0 / total  for key in l]
    labels = ['{0} - {1:1.2f} %'.format(s, p) for s, p in zip(minors, percentage) ]
    fig1, ax1 = plt.subplots()
    p = ax1.pie(values, startangle=90)
    ax1.axis('equal')
    plt.legend(p[0], labels, bbox_to_anchor=(1, 0.5), loc="right",
               bbox_transform=plt.gcf().transFigure)
    plt.subplots_adjust(left=0.0, bottom=0.1, right=0.575)
    plt.suptitle(o['major'] + ' - ' + t + '\n' +
                 str(month) + '/' + str(year) +
                 ' Total ' + str(total), ha='right')
    plt.savefig(file_name, bbox_inches='tight')
    print(t, 'image saved with file name:', file_name)
