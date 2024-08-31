import numpy as np
import tensorflow as tf

class DNASOptimizer:
    def __init__(self, input_shape, num_classes):
        self.input_shape = input_shape
        self.num_classes = num_classes
    
    def create_model(self, architecture):
        model = tf.keras.Sequential()
        model.add(tf.keras.layers.Input(shape=self.input_shape))
        
        for layer in architecture:
            if layer['type'] == 'conv2d':
                model.add(tf.keras.layers.Conv2D(layer['filters'], layer['kernel_size'], activation='relu'))
                if layer.get('pool_size'):
                    model.add(tf.keras.layers.MaxPooling2D(layer['pool_size']))
            elif layer['type'] == 'dense':
                model.add(tf.keras.layers.Dense(layer['units'], activation='relu'))
        
        model.add(tf.keras.layers.Flatten())
        model.add(tf.keras.layers.Dense(self.num_classes, activation='softmax'))
        return model
    
    def mutate_architecture(self, architecture):
        mutated = architecture.copy()
        mutation_type = np.random.choice(['add', 'remove', 'modify'])
        
        if mutation_type == 'add' and len(mutated) < 10:
            new_layer = {'type': np.random.choice(['conv2d', 'dense'])}
            if new_layer['type'] == 'conv2d':
                new_layer.update({
                    'filters': np.random.randint(16, 128),
                    'kernel_size': np.random.choice([(3, 3), (5, 5)]),
                    'pool_size': (2, 2) if np.random.random() > 0.5 else None
                })
            else:
                new_layer['units'] = np.random.randint(32, 256)
            mutated.insert(np.random.randint(0, len(mutated)), new_layer)
        elif mutation_type == 'remove' and len(mutated) > 1:
            del mutated[np.random.randint(0, len(mutated))]
        elif mutation_type == 'modify':
            layer_to_modify = np.random.randint(0, len(mutated))
            if mutated[layer_to_modify]['type'] == 'conv2d':
                mutated[layer_to_modify]['filters'] = np.random.randint(16, 128)
            else:
                mutated[layer_to_modify]['units'] = np.random.randint(32, 256)
        
        return mutated
    
    def optimize(self, x_train, y_train, x_val, y_val, population_size=20, generations=50):
        population = [
            [{'type': 'conv2d', 'filters': 32, 'kernel_size': (3, 3), 'pool_size': (2, 2)},
             {'type': 'dense', 'units': 64}]
            for _ in range(population_size)
        ]
        
        for generation in range(generations):
            fitness_scores = []
            for architecture in population:
                model = self.create_model(architecture)
                model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
                history = model.fit(x_train, y_train, epochs=5, validation_data=(x_val, y_val), verbose=0)
                fitness_scores.append(history.history['val_accuracy'][-1])
            
            elite = [population[i] for i in np.argsort(fitness_scores)[-2:]]
            new_population = elite.copy()
            
            while len(new_population) < population_size:
                parent = population[np.random.choice(len(population))]
                child = self.mutate_architecture(parent)
                new_population.append(child)
            
            population = new_population
        
        best_architecture = population[np.argmax(fitness_scores)]
        best_model = self.create_model(best_architecture)
        return best_model, best_architecture