from processor.moving_average_processor import MovingAverageProcessor, InvalidWindowSizeException, InvalidElementException

import collections
import functools

import pytest

class TestMovingAverageProcessor():
	WINDOW_SIZE = 10

	def setup_class(self):
		self.map = MovingAverageProcessor()

	# ensure creating a new window returns an empty instance of collections.deque
	def test_create_window(self):
		w = self.map.create_window(self.WINDOW_SIZE)

		assert type(w) == collections.deque
		assert len(w)  == 0

	# ensure creating a new window with an invalid size returns an empty instance of collections.deque
	def test_create_window_invalid_size(self):
		with pytest.raises(InvalidWindowSizeException):
			w = self.map.create_window(-self.WINDOW_SIZE)

	def test_add_to_window(self):
		w = self.map.create_window(self.WINDOW_SIZE)

		l = []
		for i in range(1, self.WINDOW_SIZE + 10):
			e = {'count': i, 'sum': i}
			self.map.add_to_window(w, e)
			l += [e]

			assert len(w)  == min(i, self.WINDOW_SIZE)
			assert list(w) == l[-self.WINDOW_SIZE:]

	def test_add_to_window_invalid_element(self):
		w = self.map.create_window(self.WINDOW_SIZE)

		with pytest.raises(InvalidElementException):
			self.map.add_to_window(w, 1)


	def test_compute_average(self):
		w = self.map.create_window(self.WINDOW_SIZE)

		l = []
		for i in range(1, self.WINDOW_SIZE):
			e = {'count': i, 'sum': i}
			self.map.add_to_window(w, e)
			l += [e]

		acc_sum   = functools.reduce(lambda acc, e: acc + e['sum'],   l[-self.WINDOW_SIZE:], 0)
		acc_count = functools.reduce(lambda acc, e: acc + e['count'], l[-self.WINDOW_SIZE:], 0)

		assert self.map.compute_average(w) == acc_sum / acc_count

	def test_compute_average_empty_window(self):
		w = self.map.create_window(self.WINDOW_SIZE)

		assert self.map.compute_average(w)  == 0
