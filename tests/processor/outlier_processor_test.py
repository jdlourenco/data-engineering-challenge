from processor.outlier_processor import OutlierProcessor
from adapter.outlier_adapter import OutlierAdapter
from reader.json_file_reader import JsonFileReader

import random

class TestOutlierProcessor():
	INPUT_FILE = 'events.json'
	EVENT_NAME = 'translation_delivered'

	def setup_class(self):
		self.data = OutlierAdapter().adapt({
			'data_frame': JsonFileReader().read(self.INPUT_FILE),
			'event_name': self.EVENT_NAME
		})
		self.op = OutlierProcessor()

	def test_process(self):
		pass

	def test_compute_mean(self): 
		mean = self.op.compute_mean(self.data)

		# compute_stdev returns a float
		assert type(mean) == float

	def test_compute_stdev(self):
		stdev = self.op.compute_stdev(self.data)

		# compute_stdev returns a float
		assert type(stdev) == float
		
	def test_get_outliers(self):
		outliers = self.op.get_outliers(self.data, random.uniform(1, 30), random.uniform(1, 30))
	
		# get_outliers returns a list of dicts
		assert type(outliers) == list

		for entry in outliers:
			assert type(entry) == dict
