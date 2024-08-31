import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.quantum_info import partial_trace, entropy, Statevector
from qiskit.circuit.library import RXGate, RYGate, RZGate, CXGate
from qiskit_aer import AerSimulator
from qiskit_algorithms.optimizers import COBYLA
from typing import List, Tuple

class EntanglementOptimizer:
    def __init__(self, num_qubits: int):
        self.num_qubits = num_qubits
        self._simulator = AerSimulator(method='statevector')
    
    def generate_parameterized_circuit(self) -> Tuple[QuantumCircuit, List[float]]:
        qr = QuantumRegister(self.num_qubits)
        cr = ClassicalRegister(self.num_qubits)
        circuit = QuantumCircuit(qr, cr)
        params = []

        for qubit in range(self.num_qubits):
            rx_param = np.random.random() * 2 * np.pi
            ry_param = np.random.random() * 2 * np.pi
            rz_param = np.random.random() * 2 * np.pi
            params.extend([rx_param, ry_param, rz_param])
            
            circuit.append(RXGate(rx_param), [qr[qubit]])
            circuit.append(RYGate(ry_param), [qr[qubit]])
            circuit.append(RZGate(rz_param), [qr[qubit]])

        for qubit in range(self.num_qubits - 1):
            circuit.append(CXGate(), [qr[qubit], qr[qubit + 1]])

        return circuit, params
    
    def measure_entanglement(self, circuit: QuantumCircuit) -> float:
        statevector = Statevector.from_instruction(circuit)
        
        reduced_density_matrix = partial_trace(statevector, [0])
        return entropy(reduced_density_matrix)
    
    def objective_function(self, params: List[float], circuit: QuantumCircuit) -> float:
        bound_circuit = circuit.bind_parameters(params)
        return -self.measure_entanglement(bound_circuit)  # Negative because we want to maximize
    
    def optimize_entanglement(self, num_iterations: int) -> Tuple[QuantumCircuit, float]:
        circuit, initial_params = self.generate_parameterized_circuit()
        
        optimizer = COBYLA(maxiter=num_iterations)
        result = optimizer.optimize(len(initial_params), 
                                    lambda p: self.objective_function(p, circuit),
                                    initial_point=initial_params)
        
        best_params, best_entanglement = result
        best_circuit = circuit.bind_parameters(best_params)
        
        return best_circuit, -best_entanglement  # Negate entanglement because we maximized the negative
    
    def analyze_entanglement(self, circuit: QuantumCircuit) -> dict:
        entanglement = self.measure_entanglement(circuit)
        statevector = Statevector.from_instruction(circuit)
        
        analysis = {
            "entanglement": entanglement,
            "statevector": statevector,
            "circuit_depth": circuit.depth(),
            "circuit_width": circuit.width()
        }
        
        return analysis