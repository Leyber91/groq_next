class DynamicRouter:
    def __init__(self, model_pool, rate_limiter):
        self.model_pool = model_pool
        self.rate_limiter = rate_limiter
    
    def select_model(self, input_text):
        available_models = self.rate_limiter.get_available_models()
        return self.model_pool.get_best_model(input_text, available_models)