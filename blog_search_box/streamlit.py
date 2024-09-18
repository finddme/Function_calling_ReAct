"""
command:
streamlit run streamlit_fastapi.py

http://192.168.2.186:8501/
"""
import asyncio
import streamlit as st
import requests
import json
import io
from functools import reduce

async def get_response(user_input):
    client="http://eleven.acryl.ai:37808/chat"
    headers = { 'Content-Type': 'application/json' }
    user_input={"user_input": user_input}
    response = requests.request("POST", client , headers=headers, data=json.dumps(user_input))
    return response

async def run_convo():
    # st.title(""":blue[Multi-Agent search box]""")
    st.markdown("""
    <style>
    .small-font {
        font-size:12px !important;
        color:gray;
        margin-top: 0%;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown("""**검색어를 입력하세요.**\\
                :orange[**Law | Finance | Ai | Conversation | web search | Image generation**]""", 
                unsafe_allow_html=True 
                )
    user_input = st.text_input('')

    if user_input:
        with st.spinner("Processing..."):
            response = await get_response(user_input)
            try:
                try:
                    answer = response.json()['output']
                    agent = response.json()['agent'][0]
                    observation=response.json()['observation']
                    log=response.json()['log']
                    
                    # result=f"""**Action: [{agent.title()}]**\\
                    #         \\
                    #         {answer}\\
                    #         ----------------------------------------------------\\
                    #         **Observation**\\
                    #         <p class='small-font'>{observation}<\p>
                    #         """
                    
                    result=f"""**Action: [{agent.title()}]**\\
                            \\
                            {answer}\\
                            =====================================================================\\
                            =====================================================================\\
                            **LOG**\\
                            \\
                            <p class='small-font'>
                            """
                    for l in log:
                        if "[INFO] Response:" in l: pass
                        else:
                            result+=f"{l}"
                        result+=f"<br>"
                    # result+="<\p>"
                    st.markdown(result,unsafe_allow_html=True)

                except Exception as e:
                    img = response.content
                    st.image(io.BytesIO(img).getvalue(), caption="Sunrise by the mountains")
            except Exception as e:
                st.error(f"Error: {e}")
    st.image("https://finddme.github.io/public/fc_react.png", caption="search box pipeline")
    
if __name__ == '__main__':
    asyncio.run(run_convo())

