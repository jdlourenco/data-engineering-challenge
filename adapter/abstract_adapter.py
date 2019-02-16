from abc import ABC, abstractmethod

class AbstractAdapter(ABC):

	@abstractmethod
	def adapt(self, params):
		pass
