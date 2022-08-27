import sys
import option_handler
import file_name_processor
import data_reader
import counts_processor

def main():
	options = option_handler.CollectOptions()
	file_name_processor.CollectFiles(options)
	file_name_processor.VetBoundingMonths(options)
	if not data_reader.ReadData(options):
		# ReadData will have printed something if a 
		# catastrophic error occurred.
		sys.exit(1)

	counts_processor.Counts(options)
	counts_processor.Breakdown(options)

if __name__ == '__main__':
	main()
