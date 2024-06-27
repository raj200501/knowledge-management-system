import transformers

class KnowledgeLLM:
    def __init__(self, model_name='distilbert-base-uncased'):
        self.tokenizer = transformers.AutoTokenizer.from_pretrained(model_name)
        self.model = transformers.AutoModelForSequenceClassification.from_pretrained(model_name)

    def classify(self, text):
        inputs = self.tokenizer(text, return_tensors='pt')
        outputs = self.model(**inputs)
        return outputs.logits.argmax().item()

# Example usage
llm = KnowledgeLLM()
print(llm.classify("Sample text for classification."))
