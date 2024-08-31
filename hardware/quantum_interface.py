from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

class QuantumInterface:
    def __init__(self, num_qubits):
        self.num_qubits = num_qubits
        self.backend = AerSimulator()
    
    def create_circuit(self):
        return QuantumCircuit(self.num_qubits)
    
    def apply_gate(self, circuit, gate, qubit):
        if gate == 'H':
            circuit.h(qubit)
        elif gate == 'X':
            circuit.x(qubit)
        elif gate == 'Y':
            circuit.y(qubit)
        elif gate == 'Z':
            circuit.z(qubit)
        return circuit
    
    def apply_controlled_gate(self, circuit, gate, control, target):
        if gate == 'CX':
            circuit.cx(control, target)
        elif gate == 'CZ':
            circuit.cz(control, target)
        return circuit
    
    def measure(self, circuit):
        circuit.measure_all()
        transpiled_circuit = transpile(circuit, self.backend)
        job = self.backend.run(transpiled_circuit, shots=1000)
        result = job.result()
        counts = result.get_counts(circuit)
        return counts