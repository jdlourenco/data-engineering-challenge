from processor.abstract_processor import AbstractProcessor

import collections
import datetime

class MovingAverageProcessor(AbstractProcessor):

	PARAMS    = ['input_data', 'window_size', 'column', 'writer']
	EMPTY_ROW = {'sum': 0, 'count':0}

	def process(self, params):
		[ input_data, window_size, column, writer ] = map(params.get, self.PARAMS)

		window = self.create_window(window_size)

		current_ts = None
		for row in input_data:
			window = self.add_to_window(window, row)
			moving_average = self.compute_average(window)

			current_ts = row['timestamp'] + datetime.timedelta(minutes=1)

			writer.write({ 'date': current_ts, f'avg_last{window_size}m_{column}': moving_average})

		# fill in empty data windows while moving average is not zero
		while True:
			window = self.add_to_window(window, self.EMPTY_ROW)
			moving_average = self.compute_average(window)

			if moving_average == 0:
				break

			current_ts += datetime.timedelta(minutes=1)

			writer.write({ 'date': current_ts, f'avg_last{window_size}m_{column}': moving_average})

	def create_window(self, window_size):
		return collections.deque(maxlen=window_size)

	def add_to_window(self, window, el):
		window.append(el)

		return window

	def compute_average(self, window):
		acc_sum   = sum([x['sum']   for x in window])
		acc_count = sum([x['count'] for x in window])

		return 0 if acc_count == 0 else acc_sum / acc_count
