from groq import Groq

class GemmaModel:
    def __init__(self, config):
        self.config = config
        self.client = Groq()
    
    def generate(self, input_text):
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": input_text}],
            model="gemma-7b-it",
            max_tokens=self.config["max_tokens"]
        )
        return response.choices[0].message.content
    
    def score(self, input_text):
        return len(input_text) / self.config['max_tokens']