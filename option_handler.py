from getopt import getopt, GetoptError
import sys

def __PrintHelp(print_newline = True):
	options = [
		('option',      'argument',  'meaning'),
		('help',        'none',      'prints this help text'),
		('folder',      'path',      'required - specifies path to folder containing the data'),
		('major',       'major',     'required - specifies major of focus'),
		('', '', ''),
		('start_month', 'file name', 'for reports that have a definable range of months, this is the start'),
		('end_month',   'file name', 'for reports that have a definable range of months, this is the end'),
		('', '', ''),
		('counts',      'none',      'emits counts of majors and minors broken down by academic level'),
		('breakdown',   'none',      'emits counts broken down by cohort'),
		('gpa',         'cohort',    'all, FF, SO, JR, or SR'),
		('gpa_lt',      'float',     'modifies --gpa to show only GPAs < value'),
        ('gpa_ge',      'float',     'modifies --gpa to show only GPAs >= value'),
		('email',       'cohort',    'email addresses of minors'),
		('EMAIL',       'cohort',    'email addresses of majors'),
		('', '', ''),
		('Pairings',    'none',      'emits double major counts'),
		('pairings',    'none',      'emits counts of minors'),
		('Locate',      'major 2',   'searches for students in both majors in end_month'),
		('locate',      'minor',     'searches for students in major and minor in end_month'),
		('reverse_Locate', 'major',  'ignores --major - find students with either major as specified'),
		('reverse_locate', 'minor',  'ignores --major - find any student minoring as specified'),
		('', '', ''),
		('graph',       'none',      'switch from text to graph, if possible'),
		('term',        'term',      'for some reports, consider only the given term'),
		('quiet',       'none',      'if given, text reports do not have headers'),
		('csv',         'none',      'give for text reports destined for Excel, etc.'),
	]
	if print_newline:
		print()

	print('Usage:')
	for l in options:
		print('{:<15s}{:<21s}{:s}'.format(l[0], l[1], l[2]))

def CollectOptions() -> dict:
	short_opts = ''
	long_opts = [
		'help',
		'folder=',
		'major=',
		'start_month=',
		'end_month=',
		'gpa=',
		'email=',
		'EMAIL=',
		'gpa_lt=',
        'gpa_ge=',
		'counts',
		'breakdown',
		'term=',
		'quiet',
		'Pairings',
		'pairings',
		'graph',
		'Locate=',
		'locate=',
		'reverse_Locate=',
		'reverse_locate=',
		'csv',
	]

	o = { }
	o['major'] = ''
	o['minor'] = ''
	o['folder'] = ''
	o['start_month'] = ''
	o['end_month'] = ''
	o['term'] = ''
	o['do_counts'] = False
	o['do_breakdown'] = False
	o['do_Pairings'] = False
	o['do_pairings'] = False
	o['do_Locate'] = ''
	o['do_locate'] = ''
	o['do_reverse_Locate'] = ''
	o['do_reverse_locate'] = ''
	o['do_gpa'] = ''
	o['gpa_lt'] = ''
	o['gpa_ge'] = ''
	o['do_email'] = ''
	o['do_EMAIL'] = ''
	o['quiet'] = False
	o['graph'] = False
	o['csv'] = False

	try:
		opts, _ = getopt(sys.argv[1:], short_opts, long_opts)
	except GetoptError as ex:
		print(ex)
		__PrintHelp(False)
		exit(1)

	for opts, arg in opts:
		if opts in ('--help'):
			__PrintHelp(False)
			sys.exit(0)
		elif opts in ('--folder'):
			o['folder'] = arg.strip()
		elif opts in ('--major'):
			o['major'] = arg.strip()
		elif opts in ('--minor'):
			o['minor'] = arg.strip()
		elif opts in ('--start_month'):
			o['start_month'] = arg.strip() + '.csv'
		elif opts in ('--end_month'):
			o['end_month'] = arg.strip() + '.csv'
		elif opts in ('--term'):
			o['term'] = arg.strip()
		elif opts in ('--gpa'):
			o['do_gpa'] = arg.strip()
		elif opts in ('--gpa_lt'):
			o['gpa_lt'] = arg.strip()
		elif opts in ('--gpa_ge'):
			o['gpa_ge'] = arg.strip()
		elif opts in ('--Locate'):
			o['do_Locate'] = arg.strip()
		elif opts in ('--locate'):
			o['do_locate'] = arg.strip()
		elif opts in ('--reverse_Locate'):
			o['do_reverse_Locate'] = arg.strip()
		elif opts in ('--reverse_locate'):
			o['do_reverse_locate'] = arg.strip()
		elif opts in ('--counts'):
			o['do_counts'] = True
		elif opts in ('--breakdown'):
			o['do_breakdown'] = True
		elif opts in ('--quiet'):
			o['quiet'] = True
		elif opts in ('--graph'):
			o['graph'] = True
		elif opts in ('--Pairings'):
			o['do_Pairings'] = True
		elif opts in ('--pairings'):
			o['do_pairings'] = True
		elif opts in ('--email'):
			o['do_email'] = arg.strip()
		elif opts in ('--EMAIL'):
			o['do_EMAIL'] = arg.strip()
		elif opts in ('--csv'):
			o['csv'] = True
			o['quiet'] = True

	if o['folder'] == '':
		print('Error: --folder must be specified.', file=sys.stderr)
		__PrintHelp()
		sys.exit(1)

	if o['major'] == '':
		print('Error: --major must be specified.', file=sys.stderr)
		__PrintHelp()
		sys.exit(1)

	if o['gpa_lt'] != '' and o['gpa_ge'] != '':
		print('Error: --gpa_lt and --gpa_ge cannot be used together.', file=sys.stderr)
		__PrintHelp()
		sys.exit(1)

	terms = ('j-term', 'fall', 'spring', 'summer')
	if o['term'] != '' and o['term'] not in terms:
		print('Error: term must be one of', terms, file=sys.stderr)
		sys.exit(1)

	__CheckCohort(o, 'do_gpa', '--gpa')
	__CheckCohort(o, 'do_email', '--email')
	__CheckCohort(o, 'do_EMAIL', '--EMAIL')

	if (o['do_email'] or o['do_EMAIL']) and o['graph']:
		print('Error: neither --email nor --EMAIL have graphs', file=sys.stderr)
		sys.exit(1)
		
	if o['do_gpa'] != '' and o['graph']:
		print('Error: --gpa does not have a corresponding graph', file=sys.stderr)
		sys.exit(1)

	if o['do_gpa'] == '' and o['gpa_le'] != '':
		print('Error: --gpa_le requires --gpa or --email', file=sys.stderr)
		sys.exit(1)

	if o['minor'] == '':
		o['minor'] = o['major']

	if o['do_Locate'] != '' and o['do_locate'] != '':
		print('Error: cannot specify both --Locate and --locate', file=sys.stderr)
		sys.exit(1)

	if (o['do_Locate'] != '' or o['do_locate'] != '') and o['graph']:
		print('Error: no graph associated with --Locate or --locate', file=sys.stderr)
		sys.exit(1)

	if (o['do_reverse_Locate'] != '' or o['do_reverse_locate'] != '') and o['graph']:
		print('Error: no graph associated with --reverse_Locate or --reverse_locate', file=sys.stderr)
		sys.exit(1)

	return o

def	__CheckCohort(o, tag, legend):
	allowable_cohorts = ('FF', 'SO', 'JR', 'SR', 'all')
	if o[tag] != '' and o[tag] not in allowable_cohorts:
		print('Error:', legend, 'with invalid cohort', file=sys.stderr)
		print('Cohort must be one of all, FR, SO, JR or SR', file=sys.stderr)
		__PrintHelp()
		sys.exit(1)

