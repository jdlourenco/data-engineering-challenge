from adapter.abstract_adapter import AbstractAdapter

class OutlierAdapter(AbstractAdapter):

	PARAMS = ['data_frame', 'column']

	def adapt(self, params):
		[data_frame, column] = map(params.get, self.PARAMS)

		data_frame = data_frame.to_dict('records')

		return data_frame
