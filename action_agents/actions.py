from .search_engine import *
from db.db_management import set_db_client
from utils.config import *
from db.retrieve import *
import random
import torch
from model.models import img_model_call,img_inference

naver_news=NAVER_NEWS()
search_engine=Search_API()
client= set_db_client()

class Action:
    @staticmethod
    def web_ko(query):
        wiki_res=search_engine.wikipedia_ko(query)
        naver_news_res=naver_news(query)
        tavily_res=search_engine.tavily(query)
        web_search_res=f"{tavily_res} \n {wiki_res} \n {naver_news_res}"
        return web_search_res

    @staticmethod
    def web_global(query):
        wiki_res=search_engine.wikipedia_en(query)
        tavily_res=search_engine.tavily(query)
        serper_res=search_engine.serper(query)
        web_search_res=f"{serper_res} \n {tavily_res} \n {wiki_res}"
        return web_search_res

    @staticmethod
    def web_finance(query):
        fn_res=naver_news.finance()
        fn_sise_res=naver_news.finance_sise_top()
        fn_sm_res=naver_news.finance_stock_market()
        fn_sise_global_res=naver_news.finance_sise_top_global()
        web_search_res=f"""최근 금융 시장 주요 뉴스: {fn_res}
                            대한민국 주식 거래 상위 종목:{fn_sise_res}
                            해외 주식 거래 상위 종목: {fn_sise_global_res}
                            증시: {fn_sm_res}"""
        return web_search_res

    @staticmethod
    def ai_retrieval(query):
        global client
        ai_weaviate_class=DB["ai_weaviate_class"]

        retrieval_res=retrieve(query,ai_weaviate_class)
        rerank_res=reranker_cohere(query,retrieval_res,ai_weaviate_class)
        return rerank_res

    @staticmethod
    def law_retrieval(query):
        global client

        law_weaviate_class=DB["law_weaviate_class"]

        retrieval_res=retrieve(query,law_weaviate_class)
        rerank_res=reranker_cohere(query,retrieval_res,law_weaviate_class)
        return rerank_res

    @staticmethod
    def image_generation(query,args,pipe,device,MAX_SEED):
        if args.image=="api":
            img_res=img_model_call(query)
        else:
            args.img_res=img_inference(pipe,device,MAX_SEED,query)
        # return {"query":query,"agent":["image generation"],"generate":img_res,"react_res":"","observations":"","iter_count":iter_count}
        return img_res

class Action_Map:
    def __init__(self,state):
        self.query=state["query"]
        self.action=state["action "]

        act_function=action_map[self.action]
        action_res=act_function(self.query)

        return action_res