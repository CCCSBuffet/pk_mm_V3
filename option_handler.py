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
		('breakdown',   'none',      'emits breakdown of cohorts'),
		('', '', ''),
		('Pairings',    'none',      'emits double major counts'),
		('pairings',    'none',      'emits counts of minors'),
		('', '', ''),
		('graph',       'none',      'switch from text to graph, if possible'),
		('term',        'term',      'for some reports, consider only the given term'),
		('quiet',       'none',      'if given, text reports do not have headers'),
	]
	if print_newline:
		print()

	print('Usage:')
	for l in options:
		print('{:<14s}{:<21s}{:s}'.format(l[0], l[1], l[2]))

def CollectOptions() -> dict:
	short_opts = ''
	long_opts = [
		'help',
		'folder=',
		'major=',
		'start_month=',
		'end_month=',
		'counts',
		'breakdown',
		'term=',
		'quiet',
		'Pairings',
		'pairings',
		'graph'
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
	o['quiet'] = False
	o['graph'] = False

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
		elif opts in ('--start_month'):
			o['start_month'] = arg.strip() + '.csv'
		elif opts in ('--end_month'):
			o['end_month'] = arg.strip() + '.csv'
		elif opts in ('--term'):
			o['term'] = arg.strip()
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

	if o['folder'] == '':
		print('Error: --folder must be specified.', file=sys.stderr)
		__PrintHelp()
		sys.exit(1)

	if o['major'] == '':
		print('Error: --major must be specified.', file=sys.stderr)
		__PrintHelp()
		sys.exit(1)

	terms = ('j-term', 'fall', 'spring', 'summer')
	if o['term'] != '' and o['term'] not in terms:
		print('Error: term must be one of', terms, file=sys.stderr)
		sys.exit(1)

	if o['minor'] == '':
		o['minor'] = o['major']

	return o
