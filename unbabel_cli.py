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
		moving_average: computes the moving average over the past N minutes aggregated in 1 minute time windows determined by the window_size option
		outliers: uses the three-sigma rule for detecting outliers
		[default=moving_average]
	'''
)
@click.option("--input_file",  type=click.Path(exists=True),  help="Input file", required=True)
@click.option("--window_size", type=int,  default=10,         help="Window size in minutes [default=10]")
@click.option("--event_name",  type=click.Choice(['translation_requested', 'translation_delivered']),
	default='translation_delivered',
	help="Filters input data considering only rows matching event name [default=translation_delivered]"
)
def run(input_file, window_size, mode, event_name):
	input_df   = read_input(input_file)
	input_data = adapt_input(mode, input_df, event_name)
	process_data(mode, input_data, window_size, event_name)

def read_input(input_file):
	return JsonFileReader().read(input_file)

def adapt_input(mode, data_frame, event_name):
	params = {
		'data_frame': data_frame,
		'event_name': event_name
	}
	adapter = MODE_ADAPTER[mode]

	return adapter().adapt(params)

def process_data(mode, input_data, window_size, event_name):
	params = {
		'input_data':  input_data,
		'window_size': window_size,
		'event_name':  event_name,
		'writer':      JsonStdoutWriter(),
	}

	processor     = MODE_PROCESSORS[mode]
	processor_obj = processor()
	processor_obj.process(params)

if __name__ == '__main__':
    run()
