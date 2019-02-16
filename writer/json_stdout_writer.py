from writer.abstract_writer import AbstractWriter

import datetime
import json

class JsonStdoutWriter(AbstractWriter):

	TIME_FMT = '%Y-%m-%d %H:%M:%S'

	def write(self, data):
		data_t = {
			k: self.datetime_to_s(v) if type(v) == datetime.datetime else v for k, v in data.items()
		}
		print(json.dumps(data_t))

	def datetime_to_s(self, datetime_obj):
		return datetime_obj.strftime(self.TIME_FMT)
