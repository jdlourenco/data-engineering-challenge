#!/usr/bin/env python3

from processor.moving_average_processor import MovingAverageProcessor
from processor.outlier_processor        import OutlierProcessor

from adapter.outlier_adapter        import OutlierAdapter
from adapter.moving_average_adapter import MovingAverageAdapter

from reader.json_file_reader import JsonFileReader
from writer.json_stdout_writer import JsonStdoutWriter

import click

MODE_PROCESSORS = {
	'moving_average': MovingAverageProcessor,
	'outliers':       OutlierProcessor,
}

MODE_ADAPTER = {
	'moving_average': MovingAverageAdapter,
	'outliers':       OutlierAdapter,
}

@click.command()
@click.option(
	"--mode", type=click.Choice(['moving_average', 'outliers']),
	default='moving_average',
	help='''
		moving_average: computes for every minute the moving average over the past X minutes determined by the window_size option
		outliers: 
		[default=moving_average]
	'''
)
@click.option("--input_file",  type=click.Path(exists=True),  help="Input file", required=True)
@click.option("--window_size", type=int,  default=10,         help="Window size in minutes [default=10]")
@click.option("--column",      type=str, default='duration', help="Window size in minutes [default=10]")
def run(input_file, window_size, mode, column):
	input_df   = read_input(input_file)
	input_data = adapt_input(mode, input_df, column)
	handle_data(mode, input_data, window_size, column)

def read_input(input_file):
	return JsonFileReader().read(input_file)

def adapt_input(mode, data_frame, column):
	params = {
		'data_frame': data_frame,
		'column': column
	}
	adapter = MODE_ADAPTER[mode]

	return adapter().adapt(params)

def handle_data(mode, input_data, window_size, column):
	params = {
		'input_data':  input_data,
		'window_size': window_size,
		'column':      column,
		'writer':      JsonStdoutWriter(),
	}

	processor     = MODE_PROCESSORS[mode]
	processor_obj = processor()
	processor_obj.process(params)

if __name__ == '__main__':
    run()

# def compute_counts_per_minute:
# 	pass

# def compute_sum_per_minute:
# 	pass

# def merge_counts_sums:
# 	pass

# def create_window(window_size):
# 	# return collections.deque(maxlen=window_size+1)
# 	return collections.deque(maxlen=window_size)

# def add_to_window(window, row):
# 	window.append(row.to_dict())

# def get_valid_values(queue):
# 	return [ el for el in queue if not math.isnan(el['count']) and not math.isnan(el['sum']) ]

# def compute_average(queue):
# 	values    = get_valid_values(queue)
# 	acc_sum   = sum([x['sum']   for x in values])
# 	acc_count = sum([x['count'] for x in values])
# 	return 0 if acc_count == 0 else acc_sum / acc_count


# def compute_moving_average(input_df, window_size_min, column):
# 	# counts = input_df.resample('1Min', on='timestamp').count()
# 	# sums = input_df.resample('1Min', on='timestamp').sum()
# 	input_df = input_df[['timestamp', column]].set_index('timestamp')
# 	counts = input_df.resample('1Min').count()
# 	counts.columns = ['count']
# 	sums = input_df.resample('1Min').sum()
# 	sums.columns = ['sum']
# 	counts_sums = sums.merge(counts, on='timestamp')

# 	# consider replacing this with slices in order to remove state
# 	# window = collections.deque(maxlen=window_size_min+1)
# 	window = create_window(window_size_min)

# 	for index, row in counts_sums.iterrows():
# 		add_to_window(window, row)
# 		moving_average = compute_average(window)

# 		print(json.dumps({'date': index.strftime(TIME_FMT), 'average_delivery_time': moving_average}))

# def outliers(input_df, window_size, column):
	
# 	mean = input_df._get_numeric_data().mean()[column]
# 	std  = input_df._get_numeric_data().std()[column]
# 	print(mean)
# 	print(std)

# 	three_sigma = mean + 3 * std

# 	# pdb.set_trace()

# 	outliers = input_df[input_df[column] > three_sigma]
# 	print(outliers)
