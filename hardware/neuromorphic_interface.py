import numpy as np

class NeuromorphicInterface:
    def __init__(self, num_neurons, num_synapses):
        self.num_neurons = num_neurons
        self.num_synapses = num_synapses
        self.weights = np.random.randn(num_neurons, num_synapses)
        self.thresholds = np.random.rand(num_neurons)
    
    def activate(self, inputs):
        if len(inputs) != self.num_synapses:
            raise ValueError("Input size must match number of synapses")
        
        potentials = np.dot(self.weights, inputs)
        spikes = (potentials > self.thresholds).astype(int)
        return spikes
    
    def update_weights(self, pre_synaptic, post_synaptic, learning_rate):
        delta_w = np.outer(post_synaptic, pre_synaptic) * learning_rate
        self.weights += delta_w
    
    def simulate(self, input_sequence, time_steps):
        results = []
        for _ in range(time_steps):
            for inputs in input_sequence:
                output = self.activate(inputs)
                self.update_weights(inputs, output, 0.01)
                results.append(output)
        return results