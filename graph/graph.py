from langgraph.graph import END, StateGraph, START
from .node import Node
from typing_extensions import TypedDict
from typing import List
from pydantic import BaseModel, Field,model_serializer
from pydantic import TypeAdapter
from typing import List
from utils.formats import GraphState

class Graph:
    def __init__(self,args):
        self.args=args
        global GraphState
        self.node=Node(self.args)
        if args.ai_db_restore=="yes":
            ai_db_reload_auto()
    def graph(self):
        global GraphState
    
        workflow = StateGraph(GraphState)
    
        # Define the nodes
        workflow.add_node("function_call", self.node.function_call_node) 
        workflow.add_node("action_run", self.node.action_node)
        workflow.add_node("generate_response", self.node.generate_node)

        workflow.add_edge("function_call", "action_run")
        workflow.add_edge("action_run", "generate_response")
        workflow.add_edge("generate_response", END)
    
        workflow.add_edge(START, "function_call")
    
        # Compile
        app = workflow.compile()
    
        return app