# Import specific functions and classes from submodules
from .main import main
from .config import GROQ_API_KEY, MODEL_CONFIGS, QUANTUM_CONFIG, NEUROMORPHIC_CONFIG
from core.recursive_moa import RecursiveMoA
from core.dynamic_router import DynamicRouter
from core.model_pool import ModelPool
from core.self_evolving_agent import SelfEvolvingAgent
from quantum.quantum_circuit_generator import QuantumCircuitGenerator
from quantum.qenas import QENAS
from quantum.entanglement_optimizer import EntanglementOptimizer
from utils.rate_limiter import RateLimiter

# Ensure no naming conflicts on imports or exports
__all__ = [
    'main',
    'GROQ_API_KEY',
    'MODEL_CONFIGS',
    'QUANTUM_CONFIG',
    'NEUROMORPHIC_CONFIG',
    'RecursiveMoA',
    'DynamicRouter',
    'ModelPool',
    'SelfEvolvingAgent',
    'QuantumCircuitGenerator',
    'QENAS',
    'EntanglementOptimizer',
    'RateLimiter'
]

# Optionally, add version information
__version__ = '1.0.0'

# Add any package-level initialization code here if needed
def initialize():
    pass

# You can also add package-level utility functions if required
def get_package_info():
    return {
        'name': 'quantum_enhanced_moa',
        'version': __version__,
        'modules': __all__
    }