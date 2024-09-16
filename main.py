import argparse
import six, os, torch
from app.app import app
import asyncio

async def main(args):
    await app(args)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--image', type=str, default='api', 
                        choices=["api","model","none"],required=False)
    parser.add_argument('--defined-action', type=list, nargs='+', 
                        default=["web_search","ai_related_search",
                                "legal_related_search","casual_conversation","image_generation"], 
                        choices=["web_search","ai_related_search",
                                "legal_related_search","casual_conversation","image_generation"], 
                        required=False)
    parser.add_argument('--llm', type=str, default='together', 
                        choices=["openai","groq","claude","together"], required=False)
    parser.add_argument('--ai-db-restore', type=str, default='no', choices=["yes","no"], required=False)

    args = parser.parse_args()

    asyncio.run(main(args))




    
