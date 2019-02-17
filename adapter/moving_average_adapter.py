from adapter.abstract_adapter import AbstractAdapter

class MovingAverageAdapter(AbstractAdapter):

	PARAMS = ['data_frame', 'event_name']

	def adapt(self, params):
		[data_frame, event_name] = map(params.get, self.PARAMS)

		filtered_data_frame = AbstractAdapter.filter_data_by_event_name(data_frame, event_name)

		counts = self.compute_counts(filtered_data_frame)
		sums   = self.compute_sums(filtered_data_frame)

		counts_sums = sums.merge(counts, on='timestamp').reset_index().to_dict('records')

		return counts_sums

	def compute_counts(self, data_frame):
		counts = data_frame[['timestamp', 'duration']].set_index('timestamp').resample('1Min').count()
		counts.columns = ['count']

		return counts

	def compute_sums(self, data_frame):
		sums = data_frame[['timestamp', 'duration']].set_index('timestamp').resample('1Min').sum()
		sums.columns = ['sum']

		return sums
