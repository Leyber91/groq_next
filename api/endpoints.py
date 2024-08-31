from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from core.recursive_moa import RecursiveMoA
from core.dynamic_router import DynamicRouter
from core.model_pool import ModelPool
from core.self_evolving_agent import SelfEvolvingAgent
from quantum.quantum_circuit_generator import QuantumCircuitGenerator
from quantum.qenas import QENAS
from quantum.entanglement_optimizer import EntanglementOptimizer
from quantum_enhanced_moa.config import MODEL_CONFIGS, QUANTUM_CONFIG
from .middleware import rate_limit_middleware, rate_limiter

app = FastAPI()

# Apply rate limiting middleware
app.middleware("http")(rate_limit_middleware)

# Initialize the MOA components
model_pool = ModelPool(MODEL_CONFIGS)
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

class Query(BaseModel):
    text: str

class Response(BaseModel):
    answer: str
    confidence: float
    quantum_enhancement: Optional[dict] = None

@app.post("/query", response_model=Response)
async def process_query(query: Query):
    try:
        result = agent.process_input(query.text)
        return Response(
            answer=result['answer'],
            confidence=result['confidence'],
            quantum_enhancement=result.get('quantum_enhancement')
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/models", response_model=List[str])
async def get_available_models():
    return model_pool.get_available_models()

@app.post("/optimize")
async def optimize_quantum_circuit():
    try:
        optimization_result = entanglement_optimizer.optimize()
        return {"message": "Quantum circuit optimized", "result": optimization_result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/stats")
async def get_stats():
    return agent.get_stats()

@app.on_event("startup")
async def startup_event():
    # Perform any necessary initialization here
    pass

@app.on_event("shutdown")
async def shutdown_event():
    # Perform any necessary cleanup here
    pass