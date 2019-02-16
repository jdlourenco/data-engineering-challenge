from reader.json_file_reader import JsonFileReader

import pandas as pd

class TestJsonFileReader():

	INPUT_FILE = 'events.json'

	def test_read(self):
		input_dataframe = JsonFileReader().read(self.INPUT_FILE)
		
		assert type(input_dataframe) == pd.DataFrame
		assert len(input_dataframe)  == 3
		assert len(input_dataframe.columns)  == 8
