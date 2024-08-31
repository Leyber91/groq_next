import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

MODEL_CONFIGS = {
    "gemma-7b-it": {"requests_per_minute": 30, "max_tokens": 15000},
    "llama3-70b-8192": {"requests_per_minute": 30, "max_tokens": 6000},
    "llama3-8b-8192": {"requests_per_minute": 30, "max_tokens": 30000},
    "mixtral-8x7b-32768": {"requests_per_minute": 30, "max_tokens": 5000},
}

QUANTUM_CONFIG = {
    "num_qubits": 10,
    "num_layers": 5,
    "optimization_steps": 100,
}

NEUROMORPHIC_CONFIG = {
    "num_neurons": 1000,
    "num_synapses": 10000,
    "learning_rate": 0.001,
}

# Ensure no naming conflicts on imports or exports
__all__ = [
    'GROQ_API_KEY',
    'MODEL_CONFIGS',
    'QUANTUM_CONFIG',
    'NEUROMORPHIC_CONFIG'
]