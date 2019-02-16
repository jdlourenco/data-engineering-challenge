from reader.abstract_reader import AbstractReader

import pandas

class JsonFileReader(AbstractReader):

	def read(self, input_file):
		data = pandas.read_json(input_file, lines=True)

		return data
