import os
os.system("pip install crawl4ai")
os.system("pip install nest-asyncio")
os.system("crawl4ai-setup")
os.system("python -m playwright install chromium")
os.system("sudo playwright install-deps ")
os.system("sudo apt-get update  -y")
os.system("sudo apt-get upgrade  -y")
os.system("npx playwright install-deps --dry-run")
os.system("""sudo apt-get install -y \
                                        libwoff1 \
                                        libopus0 \
                                        libwebp7 \
                                        libwebpdemux2 \
                                        libenchant-2-2 \
                                        libgudev-1.0-0 \
                                        libsecret-1-0 \
                                        libhyphen0 \
                                        libgdk-pixbuf2.0-0 \
                                        libegl1 \
                                        libnotify4 \
                                        libxslt1.1 \
                                        libevent-2.1-7 \
                                        libgles2 \
                                        libxcomposite1 \
                                        libatk1.0-0 \
                                        libatk-bridge2.0-0 \
                                        libepoxy0 \
                                        libgtk-3-0 \
                                        libharfbuzz-icu0 \
                                        libgstreamer-gl1.0-0 \
                                        libgstreamer-plugins-bad1.0-0 \
                                        gstreamer1.0-plugins-good \
                                        gstreamer1.0-plugins-bad \
                                        libxt6 \
                                        libxaw7 \
                                        xvfb \
                                        fonts-noto-color-emoji \
                                        libfontconfig \
                                        libfreetype6 \
                                        xfonts-cyrillic \
                                        xfonts-scalable \
                                        fonts-liberation \
                                        fonts-ipafont-gothic \
                                        fonts-wqy-zenhei \
                                        fonts-tlwg-loma-otf \
                                        fonts-freefont-ttf""")
os.system("""sudo apt-get install  -y \
          libnss3\
            libnspr4\
            libatk1.0-0\
            libatk-bridge2.0-0\
            libcups2\
            libdrm2\
            libxcomposite1\
            libxdamage1\ 
            libxfixes3\
            libxrandr2\
            libgbm1\
            libxkbcommon0\
            libpango-1.0-0\
            libcairo2\
            libasound2\
            libatspi2.0-0 
            """)

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




    
