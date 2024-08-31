class SelfEvolvingAgent:
    def __init__(self, moa):
        self.moa = moa
        self.knowledge_base = {}
        self.performance_history = []
    
    def process_input(self, input_text):
        response = self.moa.process(input_text)
        self.update_knowledge_base(input_text, response)
        return response
    
    def update_knowledge_base(self, input_text, response):
        self.knowledge_base[input_text] = response
    
    def evolve(self):
        performance = self.evaluate_performance()
        self.performance_history.append(performance)
        if len(self.performance_history) > 10:
            if performance < sum(self.performance_history[-10:]) / 10:
                self.optimize()
    
    def evaluate_performance(self):
        return len(self.knowledge_base)  # Simple example: performance based on knowledge base size
    
    def optimize(self):
        print("Agent is optimizing based on recent performance...")
        # Implement optimization logic here