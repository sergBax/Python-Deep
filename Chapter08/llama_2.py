# -*- coding: utf-8 -*-
"""Llama_2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1welDZ0D6kkt4s6-CoJC5lLclxewGe8NE

Install the prerequisites:
"""

# !pip install transformers
# !pip install accelerate

"""Login into HuggingFace, so the program can access the stored models. The Llama series requires additional registration with Meta:"""

# !huggingface-cli login

"""Do the imports:"""

import torch
from transformers import AutoTokenizer, pipeline

"""Define the model identifier:"""

model = "meta-llama/Llama-2-7b-chat-hf"

"""Load the tokenizer:"""

tokenizer = AutoTokenizer.from_pretrained(model)

print(tokenizer)

"""Instantiate text generation pipeline:"""

text_gen_pipeline = pipeline(
    task='text-generation',
    model=model,
    tokenizer=tokenizer,
    torch_dtype=torch.bfloat16,
    device_map='auto',
)

print(text_gen_pipeline.model)

sequences = text_gen_pipeline(
    text_inputs='What is the answer to the ultimate question of life, the universe, and everything?',
    max_new_tokens=100,
    num_beams=2,
    top_k=2,
    top_p=0.8,
    do_sample=True,
    num_return_sequences=2,
    early_stopping=True
)
for s in sequences:
    print(f"RESULT: {s['generated_text']}")

print(sequences)