import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Statevector
from qiskit.circuit.library import RXGate, RYGate, RZGate, CXGate
from qiskit_algorithms.optimizers import COBYLA
from qiskit.circuit import Parameter
from typing import List, Tuple

class QENAS:
    def __init__(self, num_qubits: int, num_layers: int):
        self.num_qubits = num_qubits
        self.num_layers = num_layers
        self._simulator = AerSimulator()
    
    @property
    def simulator(self):
        return self._simulator

    def generate_parameterized_circuit(self) -> Tuple[QuantumCircuit, List[Parameter]]:
        qr = QuantumRegister(self.num_qubits)
        cr = ClassicalRegister(self.num_qubits)
        circuit = QuantumCircuit(qr, cr)
        params = []
        
        for layer in range(self.num_layers):
            for qubit in range(self.num_qubits):
                rx_param = Parameter(f'rx_{layer}_{qubit}')
                ry_param = Parameter(f'ry_{layer}_{qubit}')
                rz_param = Parameter(f'rz_{layer}_{qubit}')
                params.extend([rx_param, ry_param, rz_param])
                
                circuit.append(RXGate(rx_param), [qr[qubit]])
                circuit.append(RYGate(ry_param), [qr[qubit]])
                circuit.append(RZGate(rz_param), [qr[qubit]])
            
            for qubit in range(self.num_qubits - 1):
                circuit.append(CXGate(), [qr[qubit], qr[qubit + 1]])
        
        circuit.measure(qr, cr)
        return circuit, params
    
    def evaluate_circuit(self, circuit: QuantumCircuit, params: List[float]) -> float:
        bound_circuit = circuit.bind_parameters({param: np.random.random() * 2 * np.pi for param in params})
        statevector = Statevector.from_instruction(bound_circuit)
        return np.abs(statevector[0])**2  # Simple fitness function
    
    def objective_function(self, params: List[float], circuit: QuantumCircuit) -> float:
        bound_circuit = circuit.bind_parameters({p: v for p, v in zip(circuit.parameters, params)})
        return -self.evaluate_circuit(bound_circuit, params)  # Negative because we want to maximize
    
    def optimize(self, num_iterations: int) -> Tuple[QuantumCircuit, float]:
        circuit, params = self.generate_parameterized_circuit()
        initial_params = np.random.random(len(params)) * 2 * np.pi
        
        optimizer = COBYLA(maxiter=num_iterations)
        result = optimizer.optimize(len(initial_params), 
                                    lambda p: self.objective_function(p, circuit),
                                    initial_point=initial_params)
        
        best_params, best_fitness = result
        best_circuit = circuit.bind_parameters({p: v for p, v in zip(params, best_params)})
        
        return best_circuit, -best_fitness  # Negate fitness because we maximized the negative
    
    def run_on_simulator(self, circuit: QuantumCircuit, shots: int = 1000) -> dict:
        job = self.simulator.run(circuit, shots=shots)
        result = job.result()
        counts = result.get_counts(circuit)
        return counts