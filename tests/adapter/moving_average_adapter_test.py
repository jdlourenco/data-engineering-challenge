from adapter.moving_average_adapter import MovingAverageAdapter
from reader.json_file_reader import JsonFileReader

import pandas as pd

class TestMovingAverageAdapter():

	INPUT_FILE = 'events.json'
	EVENT_NAME = 'translation_delivered'

	COUNTS_COLUMNS = ['count']
	SUMS_COLUMNS   = ['sum']

	DATA_KEYS  = [
		'sum',
		'timestamp',
		'count'
	]

	def setup_class(self):
		self.data_frame = JsonFileReader().read(self.INPUT_FILE)
		self.maa = MovingAverageAdapter()

	def test_adapt(self):
		params = {
			'data_frame': self.data_frame,
			'event_name': self.EVENT_NAME
		}

		data = self.maa.adapt(params)

		# adapt returns a list
		assert type(data) == list

		for entry in data:
			# each list entry is a dict which keys are equal to DATA_KEYS
			assert type(entry)       == dict
			assert set(entry.keys()) == set(self.DATA_KEYS)

	def test_compute_counts(self):
		counts = self.maa.compute_counts(self.data_frame)

		# compute_counts returns a pandas DataFrame with a single counts column and index timestamp
		assert type(counts)        == pd.DataFrame
		assert len(counts.columns) == 1
		assert set(counts.columns) == set(self.COUNTS_COLUMNS)
		assert counts.index.name   == 'timestamp'

	def test_compute_sums(self):
		sums = self.maa.compute_sums(self.data_frame)

		# compute_sums returns a pandas DataFrame with a single sums column and index timestamp
		assert type(sums)        == pd.DataFrame
		assert len(sums.columns) == 1
		assert set(sums.columns) == set(self.SUMS_COLUMNS)
		assert sums.index.name   == 'timestamp'
