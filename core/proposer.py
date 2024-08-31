import random

class Proposer:
    def __init__(self, model_pool):
        self.model_pool = model_pool

    def propose(self, input_text):
        available_models = self.model_pool.get_available_models()
        proposed_models = random.sample(available_models, min(3, len(available_models)))
        return [self.model_pool.models[model].generate(input_text) for model in proposed_models]