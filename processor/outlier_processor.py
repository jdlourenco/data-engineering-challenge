from processor.abstract_processor import AbstractProcessor

import statistics

class OutlierProcessor(AbstractProcessor):

	PARAMS = ['input_data', 'event_name', 'writer']

	def process(self, params):
		[input_data, event_name, writer] = map(params.get, self.PARAMS)
		
		mean    = self.compute_mean(input_data)
		std_dev = self.compute_stdev(input_data)

		print(f'3sigma outlier detector on event_name=\'{event_name}\': mean={round(mean, 3)} stdev={round(std_dev, 3)}')

		for outlier in self.get_outliers(input_data, mean, std_dev):
			writer.write(outlier)

	def compute_mean(self, data):
		mean = statistics.mean(map(lambda v: v['duration'], data))

		return float(mean)

	def compute_stdev(self, data):
		std_dev = statistics.stdev(map(lambda v: v['duration'], data))

		return float(std_dev)

	def get_outliers(self, data, mean, std_dev):
		three_sigma = mean + 3 * std_dev

		return [ entry for entry in data if entry['duration'] > three_sigma ]
