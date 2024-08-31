import numpy as np
import tensorflow as tf

class ArchitectureSearch:
    def __init__(self, input_shape, num_classes):
        self.input_shape = input_shape
        self.num_classes = num_classes
    
    def generate_random_architecture(self):
        model = tf.keras.Sequential()
        model.add(tf.keras.layers.Input(shape=self.input_shape))
        
        num_layers = np.random.randint(1, 5)
        for _ in range(num_layers):
            layer_type = np.random.choice(['dense', 'conv2d', 'lstm'])
            if layer_type == 'dense':
                model.add(tf.keras.layers.Dense(np.random.randint(32, 256), activation='relu'))
            elif layer_type == 'conv2d':
                model.add(tf.keras.layers.Conv2D(np.random.randint(16, 128), (3, 3), activation='relu'))
                model.add(tf.keras.layers.MaxPooling2D((2, 2)))
            elif layer_type == 'lstm':
                model.add(tf.keras.layers.LSTM(np.random.randint(32, 128), return_sequences=True))
        
        model.add(tf.keras.layers.Flatten())
        model.add(tf.keras.layers.Dense(self.num_classes, activation='softmax'))
        
        return model
    
    def evaluate_architecture(self, model, x_train, y_train, x_val, y_val):
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        history = model.fit(x_train, y_train, epochs=5, validation_data=(x_val, y_val), verbose=0)
        return history.history['val_accuracy'][-1]
    
    def search(self, x_train, y_train, x_val, y_val, num_iterations):
        best_model = None
        best_accuracy = 0
        
        for _ in range(num_iterations):
            model = self.generate_random_architecture()
            accuracy = self.evaluate_architecture(model, x_train, y_train, x_val, y_val)
            if accuracy > best_accuracy:
                best_model = model
                best_accuracy = accuracy
        
        return best_model, best_accuracy