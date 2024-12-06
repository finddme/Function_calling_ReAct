import argparse
import six, os, torch
from app.direct_streamlit import streamlit_app
import asyncio
from utils.doc_search import *
from utils.config import *
import os
from action_agents.search_engine import Blog
os.system("bash requierments.sh")

async def main(args):
    await streamlit_app(args)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--defined-action', type=list, nargs='+', 
                        default=["web_search","ai_related_search",
                                "casual_conversation",
                                "financial_market_search"], 
                        choices=["web_search","ai_related_search",
                                "casual_conversation",
                                "financial_market_search"], 
                        required=False)
    parser.add_argument('--llm', type=str, default='together', 
                        choices=["claude","together"], required=False)
    parser.add_argument('--web-cluster-db-update', type=str, default="False", choices=["True","False"], required=False)

    args = parser.parse_args()

    asyncio.run(main(args))




    