import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import anthropic
from utils.config import *
import openai
from openai import OpenAI
from groq import Groq
import anthropic
from together import Together
import numpy as np
import random
import torch
import gc
import string
# from diffusers import DiffusionPipeline
from huggingface_hub import login
import io
from io import BytesIO
from utils.formats import *
import instructor
import json 
from tavily import TavilyClient
import cohere
import requests

login(HF_KEY)

image_gen_endpoint= IMAGE["image_gen_endpoint"]

class LLM_Definition:
    @staticmethod
    def openai_llm():
        global Openai_API_KEY
        llm = OpenAI(api_key=Openai_API_KEY)
        return llm

    @staticmethod 
    def groq_llm():
        global GROQ_API_KEY
        llm = Groq(api_key=GROQ_API_KEY)
        return llm

    @staticmethod
    def claude_llm():
        global Claude_API_KEY
        llm = anthropic.Anthropic(api_key=Claude_API_KEY)
        return llm

    @staticmethod
    def together_llm():
        global Together_API_KEY
        llm = Together(api_key=Together_API_KEY)
        return llm

def get_embedding_openai(text, engine="text-embedding-3-large") : 
    global Openai_API_KEY
    os.environ["OPENAI_API_KEY"] =  Openai_API_KEY
    openai.api_key =os.getenv("OPENAI_API_KEY")

    # res = openai.Embedding.create(input=text,engine=engine)['data'][0]['embedding']
    embedding_client = OpenAI()
    res= embedding_client.embeddings.create(input = text, model=engine).data[0].embedding
    return res

def cohere_engine():
    global coher_API_KEY
    co = cohere.Client(coher_API_KEY)
    return co

def tavily_engine(TAVILY_API_KEY=TAVILY_API_KEY):
    tavily = TavilyClient(api_key=TAVILY_API_KEY)
    return tavily

def img_model_call(query):
    data = json.dumps({"user_input": query}) 
    headers = { 'Content-Type': 'application/json'}
    response = requests.request("POST", image_gen_endpoint, headers=headers, data=data)
    img = response.content
    return io.BytesIO(img).getvalue()

def img_inference(pipe,device,MAX_SEED,prompt, 
                seed=42, randomize_seed=False, 
                width=1024, height=1024, 
                num_inference_steps=4):
    
    if randomize_seed:
        seed = random.randint(0, MAX_SEED)
    generator = torch.Generator().manual_seed(seed)
    image = pipe(
            prompt = prompt, 
            width = width,
            height = height,
            num_inference_steps = num_inference_steps, 
            generator = generator,
            guidance_scale=0.0
    ).images[0] 
    memory_stream = io.BytesIO()
    image.save(memory_stream, format="PNG")
    memory_stream.seek(0)
    return memory_stream
