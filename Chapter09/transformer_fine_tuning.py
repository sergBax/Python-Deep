# -*- coding: utf-8 -*-
"""transformer_fine_tuning.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1wSweHK_mhA8eRz56AejPyH3iTTm11gKl

Install the dependencies:
"""

# !pip install transformers
# !pip install datasets
# !pip install accelerate
# !pip install evaluate

"""Load the rotten tomatoes movie review dataset:"""

from datasets import load_dataset
dataset = load_dataset('rotten_tomatoes')
print(dataset)

"""Load the model tokenizer:"""

from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained('distilbert-base-uncased')
print(tokenizer)

"""Tokenize the dataset:"""

tok_dataset = dataset.map(
    lambda x: tokenizer(
        text=x['text'],
        padding='max_length',
        truncation=True),
    batched=True)

"""Load the encoder-only transformer model:"""

from transformers import AutoModelForSequenceClassification
model = AutoModelForSequenceClassification.from_pretrained('distilbert-base-uncased')

"""Print the model:"""

print(model)

"""Create trainer arguments:"""

from transformers import TrainingArguments

training_args = TrainingArguments(
    output_dir='test_trainer',
    evaluation_strategy='epoch')

"""Create the accuracy metric:"""

import evaluate

accuracy = evaluate.load('accuracy')

"""Create the trainer:"""

from transformers import Trainer
import numpy as np

trainer = Trainer(
    model=model,
    train_dataset=tok_dataset['train'],
    eval_dataset=tok_dataset['test'],
    args=training_args,
    compute_metrics=
      lambda x: accuracy.compute(
          predictions=x[0],
          references=x[1]),
    preprocess_logits_for_metrics=
      lambda x, _: np.argmax(x.cpu(), axis=-1)
)

"""Train the model:"""

trainer.train()