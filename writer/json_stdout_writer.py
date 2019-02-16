from writer.abstract_writer import AbstractWriter

import json
from datetime import date, datetime

class JsonStdoutWriter(AbstractWriter):

	def write(self, data):
		print(json.dumps(data, default=DateTimeEncoder.default))

class DateTimeEncoder(json.JSONEncoder):
    def default(obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()

        return json.JSONEncoder.default(self, obj)