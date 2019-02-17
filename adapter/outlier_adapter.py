from adapter.abstract_adapter import AbstractAdapter

class OutlierAdapter(AbstractAdapter):

	PARAMS = ['data_frame', 'event_name']

	def adapt(self, params):
		[data_frame, event_name] = map(params.get, self.PARAMS)

		filtered_data_frame = AbstractAdapter.filter_data_by_event_name(data_frame, event_name)

		data_frame = filtered_data_frame.to_dict('records')

		return data_frame
