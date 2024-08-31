from abc import ABC, abstractmethod

class MoABase(ABC):
    @abstractmethod
    def process(self, input_text):
        pass

    @abstractmethod
    def update(self, feedback):
        pass

    @abstractmethod
    def evaluate(self):
        pass