from adapter.abstract_adapter import AbstractAdapter

class MovingAverageAdapter(AbstractAdapter):

	PARAMS = ['data_frame', 'column']

	def adapt(self, params):
		[data_frame, column] = map(params.get, self.PARAMS)

		counts = self.compute_counts(data_frame, column)
		sums   = self.compute_sums(data_frame, column)

		counts_sums = sums.merge(counts, on='timestamp').reset_index().to_dict('records')

		return counts_sums

	def compute_counts(self, data_frame, column):
		counts = data_frame[['timestamp', column]].set_index('timestamp').resample('1Min').count()
		counts.columns = ['count']

		return counts

	def compute_sums(self, data_frame, column):
		sums = data_frame[['timestamp', column]].set_index('timestamp').resample('1Min').sum()
		sums.columns = ['sum']

		return sums
