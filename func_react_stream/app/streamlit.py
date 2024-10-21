"""
command:
streamlit run streamlit.py

http://192.168.2.186:8501/
"""
import asyncio
from asyncio import run_coroutine_threadsafe
from threading import Thread
import os
import sys
import streamlit as st
import requests
import random
import time
from streamlit_chat import message
from langserve import RemoteRunnable
from pprint import pprint
import json
import io
from functools import reduce

import streamlit as st
import requests
import json
import asyncio
import io
import aiohttp

# async def get_response(user_input):
#     print("user_input", user_input)
#     client = "http://192.168.2.186:7807/chat"
#     headers = {'Content-Type': 'application/json'}
#     user_input = {"user_input": user_input}
    
#     async with aiohttp.ClientSession() as session:
#         async with session.post(client, headers=headers, json=user_input) as response:
#             async for chunk in response.content.iter_any():
#                 yield chunk.decode('utf-8')

# async def run_convo():
#     st.title(""":blue[#ReAct #Multi-Agent]""")
#     st.markdown("""
#     <style>
#     .small-font {
#         font-size:12px !important;
#         color:gray;
#         margin-top: 0%;
#     }
#     </style>
#     """, unsafe_allow_html=True)
#     st.markdown(""":orange[**Law | Ai | conversation | web search | realtime | image**]""", 
#                 unsafe_allow_html=True)

#     user_input = st.text_input(' ')

#     if user_input:
#         with st.spinner("Processing..."):
#             response_placeholder = st.empty()
#             full_response = ""
#             async for chunk in get_response(user_input):
#                 full_response += chunk
#                 try:
#                     # JSON 응답 처리 시도
#                     json_response = json.loads(full_response)
#                     answer = json_response['output']
#                     agent = json_response['agent'][0]
#                     observation = json_response['observation']
                    
#                     result = f"""**Action: [{agent.title()}]**\n
#                     {answer}\n
#                     ----------------------------------------------------\n
#                     **Observation**\n
#                     <p class='small-font'>{observation}</p>
#                     """
#                     response_placeholder.markdown(result, unsafe_allow_html=True)
#                 except json.JSONDecodeError:
#                     # JSON이 아닐 경우 (이미지 등) 그대로 표시
#                     response_placeholder.text(full_response)
#                 except KeyError:
#                     # JSON이지만 예상한 키가 없는 경우
#                     response_placeholder.text(full_response)

# if __name__ == '__main__':
#     asyncio.run(run_convo())


import streamlit as st
import requests

def main():
    # st.title("Text Streaming App")
    # st.title(""":blue[#Function calling #Multi-Agent #ReACT]""")
    st.markdown("""
    <style>
    .small-font {
        font-size:12px !important;
        color:gray;
        margin-top: 0%;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown(""":orange[**Law | Finance | Ai | Conversation | Web search**]""", 
                unsafe_allow_html=True)

    api_url = "http://192.168.2.186:7807/chat" 

    user_input = st.text_input("검색어를 입력하세요:", "")

    if st.button("Enter"):
        with st.spinner("Searching for information..."):
            text_placeholder = st.empty()

            with requests.post(api_url, json={"user_input": user_input}, stream=True) as response:
                full_text = ""
                buffer = b""
                for chunk in response.iter_content(chunk_size=1):
                    if chunk:
                        buffer += chunk
                        try:
                            chunk_str = buffer.decode('utf-8')
                            full_text += chunk_str
                            text_placeholder.markdown(full_text + "▌")
                            buffer = b""
                        except UnicodeDecodeError:
                            continue

            text_placeholder.markdown(full_text)

if __name__ == "__main__":
    main()
