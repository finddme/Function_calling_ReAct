import json
import openai
from typing import List, Dict, Union
from .model_prep import Model
from utils.config import *

class Completion(Model):
    def __init__(self, llm):
        super().__init__(Completion)
        self.llm = llm
        self.model=Model(self.llm)
        self.messages = []

    def __call__(self, message, system_prompt):
        self.messages.append({"role": "system", "content":system_prompt})
        self.messages.append({"role": "user", "content": message})
        
        response = self.execute()
        return response
        
    def execute(self):
        response=self.model.__completion__(self.messages)
        return response