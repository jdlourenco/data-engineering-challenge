from adapter.abstract_adapter import AbstractAdapter

class OutlierAdapter(AbstractAdapter):

	PARAMS = ['data_frame', 'column']

	def adapt(self, params):
		[data_frame, column] = map(params.get, self.PARAMS)

		data_frame = data_frame.to_dict('records')

		return data_frame

	def compute_counts(self, data_frame):
		counts = data_frame.resample('1Min').count()
		counts.columns = ['count']

		return counts

	def compute_sums(self, data_frame):
		sums = data_frame.resample('1Min').sum()
		sums.columns = ['sum']

		return sums
