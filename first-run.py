import os
os.system("tar -xf ./emotions.zip")
os.system("del ./emotions.zip")

from transformers import pipeline, set_seed
generator = pipeline('text-generation', model='gpt2-xl', device_map="auto")
generator.save_pretrained('./chatbot-xl')
