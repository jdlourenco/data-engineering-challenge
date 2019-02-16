from adapter.abstract_adapter import AbstractAdapter

class MovingAverageAdapter(AbstractAdapter):

	PARAMS = ['data_frame', 'column']

	def adapt(self, params):
		[data_frame, column] = map(params.get, self.PARAMS)

		data_frame = data_frame[['timestamp', column]].set_index('timestamp')

		counts = self.compute_counts(data_frame)
		sums   = self.compute_sums(data_frame)

		counts_sums = sums.merge(counts, on='timestamp').to_dict('index')

		return {
			k.to_pydatetime(): v for k, v in counts_sums.items()
		}

	def compute_counts(self, data_frame):
		counts = data_frame.resample('1Min').count()
		counts.columns = ['count']

		return counts

	def compute_sums(self, data_frame):
		sums = data_frame.resample('1Min').sum()
		sums.columns = ['sum']

		return sums
