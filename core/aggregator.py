from collections import Counter

class Aggregator:
    def aggregate(self, responses):
        # Simple majority voting for demonstration
        if not responses:
            return ""
        
        words = [response.split() for response in responses]
        max_length = max(len(w) for w in words)
        
        aggregated_response = []
        for i in range(max_length):
            word_counts = Counter(words[j][i] for j in range(len(words)) if i < len(words[j]))
            if word_counts:
                aggregated_response.append(word_counts.most_common(1)[0][0])
        
        return " ".join(aggregated_response)