import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

class QuantumCircuitGenerator:
    def __init__(self, num_qubits):
        self.num_qubits = num_qubits

    def generate_random_circuit(self, depth):
        qr = QuantumRegister(self.num_qubits)
        cr = ClassicalRegister(self.num_qubits)
        circuit = QuantumCircuit(qr, cr)

        for _ in range(depth):
            # Apply random single-qubit gates
            for qubit in range(self.num_qubits):
                gate = np.random.choice(['h', 'x', 'y', 'z', 's', 't'])
                if gate == 'h':
                    circuit.h(qubit)
                elif gate == 'x':
                    circuit.x(qubit)
                elif gate == 'y':
                    circuit.y(qubit)
                elif gate == 'z':
                    circuit.z(qubit)
                elif gate == 's':
                    circuit.s(qubit)
                elif gate == 't':
                    circuit.t(qubit)

            # Apply random two-qubit gates
            if self.num_qubits > 1:
                control = np.random.randint(0, self.num_qubits)
                target = np.random.randint(0, self.num_qubits)
                while target == control:
                    target = np.random.randint(0, self.num_qubits)
                circuit.cx(control, target)

        circuit.measure(qr, cr)
        return circuit

    def generate_layered_circuit(self, num_layers):
        qr = QuantumRegister(self.num_qubits)
        cr = ClassicalRegister(self.num_qubits)
        circuit = QuantumCircuit(qr, cr)

        for _ in range(num_layers):
            # Apply Hadamard gates to all qubits
            for qubit in range(self.num_qubits):
                circuit.h(qubit)

            # Apply CNOT gates between adjacent qubits
            for qubit in range(self.num_qubits - 1):
                circuit.cx(qubit, qubit + 1)

        circuit.measure(qr, cr)
        return circuit

    def generate_entangled_circuit(self):
        qr = QuantumRegister(self.num_qubits)
        cr = ClassicalRegister(self.num_qubits)
        circuit = QuantumCircuit(qr, cr)

        circuit.h(0)
        for qubit in range(1, self.num_qubits):
            circuit.cx(0, qubit)

        circuit.measure(qr, cr)
        return circuit