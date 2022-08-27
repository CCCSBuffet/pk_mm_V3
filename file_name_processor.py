import os
import sys

def CollectFiles(options):
	files = [ ]
	if not os.path.isdir(options['folder']):
		print(options['folder'], 'is not a directory or cannot be found', file=sys.stderr)
		sys.exit(1)

	for root, _, f in os.walk(options['folder']):
		for file in f:
			if file.endswith("csv") and file.startswith('MM'):
				files.append(file)

	files.sort()

	if len(files) == 0:
		print('No CSV files found in', options['folder'], file=sys.stderr)
		sys.exit(1)

	if options['start_month'] == '':
		options['start_month'] = os.path.basename(os.path.splitext(files[0])[0]) + '.csv'

	if options['end_month'] == '':
		options['end_month'] = os.path.basename(os.path.splitext(files[-1])[0]) + '.csv'

	options['files'] = files

def VetBoundingMonths(options):
	for m in (options['start_month'], options['end_month']):
		f = str(m)
		if f not in options['files']:
			print(f, 'not found among collected files', file=sys.stderr)
			sys.exit(1)
