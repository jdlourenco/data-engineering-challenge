from processor.moving_average_processor import MovingAverageProcessor

import collections
import functools

class TestMovingAverageProcessor(object):
    # def test_one(self):
    #     x = "this"
    #     assert 'h' in x

    # def test_two(self):
    #     x = "hello"
    #     assert hasattr(x, 'check')

	def test_handle(self):
		pass

	# ensure creating a new window returns an empty instance of collections.deque
	def test_create_window(self):
		window_size = 10
		mah = MovingAverageProcessor()
		w = mah.create_window(window_size)

		assert type(w) == collections.deque
		assert len(w) == 0

	def test_add_to_window(self):
		window_size = 10
		mah = MovingAverageProcessor()
		w = mah.create_window(window_size)

		l = []
		for i in range(1, 20):
			e = {'count': i, 'sum': i}
			mah.add_to_window(w, e)
			l += [e]

			assert len(w)  == min(i, window_size)
			assert list(w) == l[-window_size:]

	def test_get_valid_values(self):
		pass

	def test_compute_average(self):
		window_size = 20
		mah = MovingAverageProcessor()
		w = mah.create_window(window_size)

		l = []
		for i in range(1, window_size):
			e = {'count': i, 'sum': i}
			mah.add_to_window(w, e)
			l += [e]

		acc_sum   = functools.reduce(lambda acc, e: acc + e['sum'],   l[-window_size:], 0)
		acc_count = functools.reduce(lambda acc, e: acc + e['count'], l[-window_size:], 0)

		assert mah.compute_average(w)  == acc_sum / acc_count

	def test_compute_average_empty_window(self):
		window_size = 10
		mah = MovingAverageProcessor()
		w   = mah.create_window(window_size)

		assert mah.compute_average(w)  == 0
