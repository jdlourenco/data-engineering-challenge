from processor.abstract_processor import AbstractProcessor

import collections
import datetime

class MovingAverageProcessor(AbstractProcessor):

	PARAMS    = ['input_data', 'window_size', 'event_name', 'writer']
	EMPTY_ROW = {'sum': 0, 'count':0}

	def process(self, params):
		[ input_data, window_size, event_name, writer ] = map(params.get, self.PARAMS)

		window = self.create_window(window_size)

		current_ts = None
		for row in input_data:
			window = self.add_to_window(window, row)
			moving_average = self.compute_average(window)

			current_ts = row['timestamp'] + datetime.timedelta(minutes=1)

			writer.write({ 'date': current_ts, f'average_{event_name}': moving_average})

		# fill in empty data windows while moving average is not zero
		while True:
			window = self.add_to_window(window, self.EMPTY_ROW)
			moving_average = self.compute_average(window)

			if moving_average == 0:
				break

			current_ts += datetime.timedelta(minutes=1)

			writer.write({ 'date': current_ts, f'average_{event_name}': moving_average})

	def create_window(self, window_size):
		if not type(window_size) == int or window_size < 1:
			raise InvalidWindowSizeException(f'Invalid window size: {window_size}')

		return collections.deque(maxlen=window_size)

	def add_to_window(self, window, el):
		if not self.__valid_el(el):
			raise InvalidElementException(f'Invalid element {el}')

		window.append(el)

		return window

	def compute_average(self, window):
		acc_sum   = sum([x['sum']   for x in window])
		acc_count = sum([x['count'] for x in window])

		return 0 if acc_count == 0 else acc_sum / acc_count

	def __valid_el(self, el):
		if not type(el) == dict:
			return False

		for k in self.EMPTY_ROW.keys():
			if not k in el.keys():
				return False

		return True

class InvalidWindowSizeException(Exception):
	pass

class InvalidElementException(Exception):
	pass