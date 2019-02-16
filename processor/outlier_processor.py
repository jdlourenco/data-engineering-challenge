from processor.abstract_processor import AbstractProcessor

class OutlierProcessor(AbstractProcessor):

	PARAMS = ['input_df', 'column']

	def process(self, params):

		[input_df, column] = map(params.get, self.PARAMS)
		
		mean = input_df._get_numeric_data().mean()[column]
		std  = input_df._get_numeric_data().std()[column]

		three_sigma = mean + 3 * std

		outliers = input_df[input_df[column] > three_sigma]
		print(outliers)