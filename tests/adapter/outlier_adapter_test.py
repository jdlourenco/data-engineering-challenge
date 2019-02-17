from adapter.outlier_adapter import OutlierAdapter
from reader.json_file_reader import JsonFileReader

class TestOutlierProcessor():

	INPUT_FILE = 'events.json'
	COLUMN     = 'duration'
	REQUIRED_DATA_KEYS  = [
		'client_name',
		'duration',
		'event_name',
		'nr_words',
		'source_language',
		'target_language',
		'timestamp',
		'translation_id'
	]
	

	def setup_class(self):
		self.data_frame = JsonFileReader().read(self.INPUT_FILE)
		self.oa = OutlierAdapter()

	def test_adapt(self):
		params = {
			'data_frame': self.data_frame,
			'column':     self.COLUMN
		}
		
		data = self.oa.adapt(params)

		# adapt returns a list
		assert type(data) == list

		for entry in data:
			# each entry in data is a dictionary
			assert type(entry) == dict

			# each dictionay has at least all REQUIRED_DATA_KEYS keys
			for key in self.REQUIRED_DATA_KEYS:
				assert key in entry.keys()
