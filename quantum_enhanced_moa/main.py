import os
from groq import Groq
from core.recursive_moa import RecursiveMoA
from core.dynamic_router import DynamicRouter
from core.model_pool import ModelPool
from core.self_evolving_agent import SelfEvolvingAgent
from utils.rate_limiter import RateLimiter
from quantum.quantum_circuit_generator import QuantumCircuitGenerator
from quantum.qenas import QENAS
from quantum.entanglement_optimizer import EntanglementOptimizer
from .config import GROQ_API_KEY, MODEL_CONFIGS, QUANTUM_CONFIG

def main():
    client = Groq(api_key=GROQ_API_KEY)
    
    model_pool = ModelPool(MODEL_CONFIGS)
    rate_limiter = RateLimiter(MODEL_CONFIGS)
    dynamic_router = DynamicRouter(model_pool, rate_limiter)
    
    quantum_circuit_generator = QuantumCircuitGenerator(num_qubits=QUANTUM_CONFIG['num_qubits'])
    qenas = QENAS(num_qubits=QUANTUM_CONFIG['num_qubits'], num_layers=QUANTUM_CONFIG['num_layers'])
    entanglement_optimizer = EntanglementOptimizer(num_qubits=QUANTUM_CONFIG['num_qubits'])
    
    moa_config = {
        'dynamic_router': dynamic_router,
        'quantum_circuit_generator': quantum_circuit_generator,
        'qenas': qenas,
        'entanglement_optimizer': entanglement_optimizer
    }
    moa = RecursiveMoA(moa_config)
    agent = SelfEvolvingAgent(moa)
    
    while True:
        user_input = input("Enter your question (or 'quit' to exit): ")
        if user_input.lower() == 'quit':
            break
        
        response = agent.process_input(user_input)
        print("Agent response:", response)
        
        agent.evolve()

if __name__ == "__main__":
    main()