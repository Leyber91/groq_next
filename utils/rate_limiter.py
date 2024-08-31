import time
from typing import Dict, List

class RateLimiter:
    def __init__(self, model_configs: Dict[str, Dict[str, int]]):
        self.model_configs = model_configs
        self.request_timestamps: Dict[str, List[float]] = {model_id: [] for model_id in model_configs}
    
    def get_available_models(self) -> List[str]:
        current_time = time.time()
        available_models = []
        
        for model_id, config in self.model_configs.items():
            self.request_timestamps[model_id] = [t for t in self.request_timestamps[model_id] if current_time - t < 60]
            if len(self.request_timestamps[model_id]) < config['requests_per_minute']:
                available_models.append(model_id)
        
        return available_models
    
    def log_request(self, model_id: str) -> None:
        self.request_timestamps[model_id].append(time.time())

    def get_remaining_requests(self, model_id: str) -> int:
        current_time = time.time()
        recent_requests = [t for t in self.request_timestamps[model_id] if current_time - t < 60]
        return self.model_configs[model_id]['requests_per_minute'] - len(recent_requests)

    def wait_for_available_request(self, model_id: str) -> None:
        while self.get_remaining_requests(model_id) == 0:
            time.sleep(1)