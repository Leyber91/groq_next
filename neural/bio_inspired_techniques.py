import numpy as np

class GeneticAlgorithm:
    def __init__(self, population_size, mutation_rate):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
    
    def initialize_population(self, gene_length):
        return [np.random.randint(0, 2, gene_length) for _ in range(self.population_size)]
    
    def fitness(self, individual):
        return np.sum(individual)  # Simple fitness function: sum of genes
    
    def select_parents(self, population, fitnesses):
        total_fitness = np.sum(fitnesses)
        probabilities = fitnesses / total_fitness
        return np.random.choice(population, size=2, p=probabilities)
    
    def crossover(self, parent1, parent2):
        crossover_point = np.random.randint(1, len(parent1) - 1)
        child = np.concatenate((parent1[:crossover_point], parent2[crossover_point:]))
        return child
    
    def mutate(self, individual):
        for i in range(len(individual)):
            if np.random.random() < self.mutation_rate:
                individual[i] = 1 - individual[i]
        return individual
    
    def evolve(self, generations):
        population = self.initialize_population(100)  # Example gene length of 100
        
        for _ in range(generations):
            fitnesses = [self.fitness(ind) for ind in population]
            new_population = []
            
            for _ in range(self.population_size // 2):
                parent1, parent2 = self.select_parents(population, fitnesses)
                child1 = self.mutate(self.crossover(parent1, parent2))
                child2 = self.mutate(self.crossover(parent2, parent1))
                new_population.extend([child1, child2])
            
            population = new_population
        
        best_individual = max(population, key=self.fitness)
        return best_individual, self.fitness(best_individual)

class ParticleSwarmOptimization:
    def __init__(self, num_particles, dimensions, bounds):
        self.num_particles = num_particles
        self.dimensions = dimensions
        self.bounds = bounds
        self.particles = np.random.uniform(bounds[0], bounds[1], (num_particles, dimensions))
        self.velocities = np.zeros((num_particles, dimensions))
        self.personal_best = self.particles.copy()
        self.global_best = self.particles[0]
        self.personal_best_fitness = np.array([self.fitness(p) for p in self.particles])
        self.global_best_fitness = self.personal_best_fitness[0]
    
    def fitness(self, particle):
        return -np.sum(particle**2)  # Simple fitness function: negative sum of squares
    
    def update(self):
        for i in range(self.num_particles):
            fitness = self.fitness(self.particles[i])
            if fitness > self.personal_best_fitness[i]:
                self.personal_best[i] = self.particles[i]
                self.personal_best_fitness[i] = fitness
            if fitness > self.global_best_fitness:
                self.global_best = self.particles[i]
                self.global_best_fitness = fitness
        
        inertia = 0.5
        cognitive = 1
        social = 2
        
        for i in range(self.num_particles):
            r1, r2 = np.random.rand(2)
            self.velocities[i] = (inertia * self.velocities[i] +
                                  cognitive * r1 * (self.personal_best[i] - self.particles[i]) +
                                  social * r2 * (self.global_best - self.particles[i]))
            self.particles[i] += self.velocities[i]
            self.particles[i] = np.clip(self.particles[i], self.bounds[0], self.bounds[1])
    
    def optimize(self, iterations):
        for _ in range(iterations):
            self.update()
        return self.global_best, self.global_best_fitness