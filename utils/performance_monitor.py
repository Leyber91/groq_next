import time
from typing import Dict

class PerformanceMonitor:
    def __init__(self):
        self.start_time = time.time()
        self.request_count = 0
        self.total_latency = 0
    
    def log_request(self, latency: float) -> None:
        self.request_count += 1
        self.total_latency += latency
    
    def get_stats(self) -> Dict[str, float]:
        elapsed_time = time.time() - self.start_time
        avg_latency = self.total_latency / self.request_count if self.request_count > 0 else 0
        requests_per_second = self.request_count / elapsed_time if elapsed_time > 0 else 0
        
        # Calculate additional performance metrics
        total_time = self.total_latency
        throughput = self.request_count / total_time if total_time > 0 else 0
        
        # Check for potential bottlenecks
        if avg_latency > 1.0:  # Arbitrary threshold, adjust as needed
            print("Warning: High average latency detected. Consider optimizing request handling.")
        
        if requests_per_second < 10:  # Arbitrary threshold, adjust as needed
            print("Warning: Low request rate detected. Consider investigating potential bottlenecks.")
        
        return {
            "total_requests": float(self.request_count),
            "average_latency": avg_latency,
            "requests_per_second": requests_per_second,
            "throughput": throughput
        }