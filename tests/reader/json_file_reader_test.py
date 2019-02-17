from reader.json_file_reader import JsonFileReader

import pandas as pd

class TestJsonFileReader():

	INPUT_FILE = 'events.json'
	REQUIRED_COLUMNS  = [
		'client_name',
		'duration',
		'event_name',
		'nr_words',
		'source_language',
		'target_language',
		'timestamp',
		'translation_id'
	]

	def test_read(self):
		input_dataframe = JsonFileReader().read(self.INPUT_FILE)
		
		# read returns a pandas dataframe with at least all REQUIRED_COLUMNS columns
		assert type(input_dataframe) == pd.DataFrame
		for key in self.REQUIRED_COLUMNS:
			assert key in input_dataframe.columns
