from model.prompt import *
from model.functions import *
from model.models import LLM_Definition
from action_agents.actions import Action

action=Action()
llm_df = LLM_Definition()

fc_mode={"openai.OpenAI":[basic_function_list,basic_toolprompt],
                "groq.Groq":[basic_function_list,llama_toolprompt],
                "anthropic.Anthropic":[claude_function_list,basic_toolprompt],
                "together.client.Together":[llama_function_list,llama_toolprompt]}


action_map={"korea_news_search":action.web_ko, 
        "global_news_search":action.web_global, 
        "financial_market_search": action.web_finance,
        "ai_related_search": action.ai_retrieval,
       "legal_related_search": action.law_retrieval}

llm_map={"openai":llm_df.openai_llm(),
        "groq":llm_df.groq_llm(),
        "claude":llm_df.claude_llm(),
        "together":llm_df.together_llm(),
        }