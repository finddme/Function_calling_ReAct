import argparse
import six, os, torch
from app.app import app
from app.direct_streamlit import streamlit_app
import asyncio
from db.db_management import ai_db_reload_auto
import os
os.system("pip install --upgrade pip")
os.system("pip install -r requierments.txt")

async def main(args):
    if args.ai_db_restore == "True":
        ai_db_reload_auto()
    if args.streamlit_direct == "True":
        streamlit_app(args)
    else:
        await app(args)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--image', type=str, default='api', 
                        choices=["api","model","none"],required=False)
    parser.add_argument('--defined-action', type=list, nargs='+', 
                        default=["web_search","ai_related_search",
                                "legal_related_search","casual_conversation",
                                "financial_market_search"], 
                        choices=["web_search","ai_related_search",
                                "legal_related_search","casual_conversation",
                                "financial_market_search"], 
                        required=False)
    parser.add_argument('--llm', type=str, default='together', 
                        choices=["openai","groq","claude","together"], required=False)
    parser.add_argument('--ai-db-restore', type=str, default="False", choices=["True","False"], required=False)
    parser.add_argument('--streamlit-direct', type=str, default="True", choices=["True","False"], required=False)

    args = parser.parse_args()

    asyncio.run(main(args))




    
