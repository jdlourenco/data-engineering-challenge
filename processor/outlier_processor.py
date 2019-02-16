from processor.abstract_processor import AbstractProcessor

import statistics

class OutlierProcessor(AbstractProcessor):

	PARAMS = ['input_data', 'column', 'writer']

	def process(self, params):
		[input_data, column, writer] = map(params.get, self.PARAMS)
		
		mean    = self.compute_mean(input_data, column)
		std_dev = self.compute_stdev(input_data, column)

		print(f'3sigma outlier detector on field=\'{column}\': mean={round(mean, 3)} stdev={round(std_dev, 3)}')

		for outlier in self.get_outliers(input_data, column, mean, std_dev):
			writer.write(outlier)

	def compute_mean(self, data, column):
		mean = statistics.mean(map(lambda v: v[column], data))

		return mean

	def compute_stdev(self, data, column):
		std_dev = statistics.stdev(map(lambda v: v[column], data))

		return std_dev

	def get_outliers(self, data, column, mean, std_dev):
		three_sigma = mean + 3 * std_dev

		return [ entry for entry in data if entry[column] > three_sigma ]
