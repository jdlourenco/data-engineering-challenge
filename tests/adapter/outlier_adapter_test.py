from adapter.outlier_adapter import OutlierAdapter
from reader.json_file_reader import JsonFileReader

class TestOutlierAdapter():

	INPUT_FILE = 'events.json'
	EVENT_NAME = 'translation_delivered'
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
			'event_name': self.EVENT_NAME
		}
		
		data = self.oa.adapt(params)

		# adapt returns a list
		assert type(data) == list

		for entry in data:
			# each entry in data is a dictionary with at least all REQUIRED_DATA_KEYS keys
			assert type(entry) == dict

			for key in self.REQUIRED_DATA_KEYS:
				assert key in entry.keys()
