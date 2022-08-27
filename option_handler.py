from getopt import getopt, GetoptError
import sys

def __PrintHelp(print_newline = True):
	options = [
		('--option', 'argument',     'meaning'),
		('help',   'none',           'prints this help text'),
		('folder', 'path to folder', 'required - specifies path to folder'),
		('',       '',               'containing the data'),
		('major',  'name of major',  'required - specifies major of focus'),
		('',       '',               'use double quotes if major contains spaces'),
		('', '', ''),
		('start_month', 'name of start month', 'for reports that have a definable'),
		('', '',                     'range of months, this is the start'),
		('end_month', 'name of end month', 'for reports that have a definable'),
		('', '',                     'range of months, this is the end'),
		('', '', ''),
		('counts', 'none',            'emits counts of majors and minors broken'),
		('', '',                      'down by academic level'),
		('', '', ''),
		('graph', 'none',             'if a report knows how to produce a chart,'),
		('', '',                      'adding this switches output from text to'),
		('', '',                      'picture'),
		('quiet', 'none',             'if given, text reports do not have headers'),
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
		'quiet',
		'graph'
	]

	o = { }
	o['major'] = ''
	o['minor'] = ''
	o['folder'] = ''
	o['start_month'] = ''
	o['end_month'] = ''
	o['do_counts'] = False
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
		elif opts in ('--counts'):
			o['do_counts'] = True
		elif opts in ('--quiet'):
			o['quiet'] = True
		elif opts in ('--graph'):
			o['graph'] = True

	if o['folder'] == '':
		print('Error: --folder must be specified.', file=sys.stderr)
		__PrintHelp()
		sys.exit(1)

	if o['major'] == '':
		print('Error: --major must be specified.', file=sys.stderr)
		__PrintHelp()
		sys.exit(1)

	if o['minor'] == '':
		o['minor'] = o['major']

	return o
