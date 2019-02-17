from abc import ABC, abstractmethod

class AbstractAdapter(ABC):

	@abstractmethod
	def adapt(self, params):
		pass

	@staticmethod
	def filter_data_by_event_name(data_frame, event_name):
		return data_frame[data_frame['event_name'] == event_name]