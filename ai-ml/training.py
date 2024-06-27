from transformers import Trainer, TrainingArguments
import torch

class TrainerWrapper:
    def __init__(self, model, tokenizer, train_dataset, eval_dataset):
        self.model = model
        self.tokenizer = tokenizer
        self.train_dataset = train_dataset
        self.eval_dataset = eval_dataset

    def train(self):
        training_args = TrainingArguments(
            output_dir='./results',          
            num_train_epochs=3,              
            per_device_train_batch_size=8,  
            per_device_eval_batch_size=8,   
            warmup_steps=500,               
            weight_decay=0.01,              
            logging_dir='./logs',            
            logging_steps=10,
        )
        
        trainer = Trainer(
            model=self.model,                
            args=training_args,                  
            train_dataset=self.train_dataset,         
            eval_dataset=self.eval_dataset            
        )

        trainer.train()

# Example usage
# Assume train_dataset and eval_dataset are already created
# model and tokenizer are instances of HuggingFace models
trainer = TrainerWrapper(model, tokenizer, train_dataset, eval_dataset)
trainer.train()
