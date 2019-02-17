from adapter.abstract_adapter import AbstractAdapter
from reader.json_file_reader import JsonFileReader

import pandas as pd

class TestAbstractAdapter():

	INPUT_FILE = 'events.json'
	EVENT_NAME_COUNTS = {
		'translation_requested': 1,
		'translation_delivered': 2,
		'xyf': 0
	}

	def setup_class(self):
		self.data_frame = JsonFileReader().read(self.INPUT_FILE)

	def test_adapt(self):
		for event_name, row_count in self.EVENT_NAME_COUNTS.items():
			filtered_data = AbstractAdapter.filter_data_by_event_name(self.data_frame, event_name)

			assert type(filtered_data) == pd.DataFrame
			assert len(filtered_data) == row_count
