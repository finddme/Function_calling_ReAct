import os
os.system("playwright install")
os.system("apt-get install libnss3\libnspr4\libatk1.0-0\libatk-bridge2.0-0\libcups2\libdrm2\libxkbcommon0\libatspi2.0-0\libxcomposite1\libxdamage1\libxfixes3\libxrandr2\libgbm1\libpango-1.0-0\libcairo2\libasound2")
import argparse
import six, torch
from app.direct_streamlit import streamlit_app
import asyncio
from utils.doc_search import *
from utils.config import *
import os
from action_agents.search_engine import Blog

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




    
