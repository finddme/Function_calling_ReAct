import argparse
import six, os, torch
# from app.app import app
from app.direct_streamlit import streamlit_app
import asyncio
# from db.db_management import ai_db_reload_auto
import os
# os.system("pip install torch==2.1.2")
# os.system("pip install Flask --ignore-installed")
# os.system("pip install xformers==0.0.23.post1")
# os.system("pip install --upgrade pip")
# os.system("pip install -r requierments.txt")

async def main(args):
    if args.web_cluster_db_update == "True":
        os.system("python ./db/db_management_webcluster.py")

    await streamlit_app(args)

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
    parser.add_argument('--web-cluster-db-update', type=str, default="False", choices=["True","False"], required=False)

    args = parser.parse_args()

    asyncio.run(main(args))




    