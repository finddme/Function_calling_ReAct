from utils.config import *
from utils.map import *
from model.prompt import *
from model.function_calling import FunctionCall
from model.completion import Completion
from utils.logging_wrapper import LoggingWrapper
from datetime import datetime

logger = LoggingWrapper('ayaan_logger')
logger.add_file_handler("info")
logger.add_stream_handler("error")

class Node:
    def __init__(self,args):
        global action_map
        global system_prompt
        global normal_completion_prompt
        global llm_map
        global log_system

        self.args=args
        if self.args.image=="model":
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            dtype = torch.float16

            self.pipe = DiffusionPipeline.from_pretrained(image_model, torch_dtype=dtype).to(device)
            self.MAX_SEED = np.iinfo(np.int32).max
            MAX_IMAGE_SIZE = 2048
        else: self.pipe,self.device,self.MAX_SEED=None,None,None

        self.llm=llm_map[self.args.llm]
        # llm=llm_map["together"]
        # self.fc = FunctionCall(self.llm)
        
        model_type = str(type(self.llm))
        self.model_type = model_type[model_type.find("'")+1:model_type.rfind("'")]

    def function_call_node(self,state):
        query=state["query"]

        today = datetime.today().strftime('%d %B %Y')

        self.fc = FunctionCall(self.llm, today)
        fc_res=self.fc(query)

        logger.info(f"Model Type: {self.model_type}")
        
        self.log_list=[]
        logger.add_list_handler(self.log_list,"info")

        logger.info(f"User Query: {query}")
        logger.info(f"Funtion Call result: {fc_res}")

        return {"query":query, "action":fc_res}

    def action_node(self,state):
        query=state["query"]
        action=state["action"]
        action_res=[]
        actions = list(map(lambda x: x['function'], action))

        if "image_generation" in actions:
            for a in action:
                if a["function"] =="image_generation":
                    act_function=action_map[a["function"]]
                    action_res.append(act_function(a["search_query"],
                                                    self.args,
                                                    self.pipe,
                                                    self.device,
                                                    self.MAX_SEED))
        else:
            for a in action:
                if a["function"] !="casual_conversation":
                    act_function=action_map[a["function"]]
                    action_res.append(act_function(a["search_query"]))
        
        return {"query":query, "action":actions, "observation": action_res}

    def generate_node(self,state):
        query=state["query"]
        action=state["action"]
        observation=state["observation"]

        self.completion=Completion(self.llm)
        
        try:
            if "image_generation" in action: 
                response,observation=observation,""

                logger.info(f"Observation: {observation}")

                pass
            else:
                for a in action:
                    if a != "casual_conversation":
                        prompt=system_prompt.format(observation)
                        # prompt=reflection_prompt.format(query,observation)
                    else:
                        if self.model_type=="anthropic.Anthropic":
                            query=f"User's question: {query} \n{normal_completion_prompt}"
                        prompt=normal_completion_prompt
                response=self.completion(query,prompt)

                response+=additional_phrase[a]             
            
                logger.info(f"Observation: {observation}")
                logger.info(f"Response: {response}")

        except Exception  as e:
            response=self.completion(query,normal_completion_prompt)

            logger.info(f"////////////\n")
            logger.info(f"Exception: {e}")
            logger.info(f"Response: {response}")
            logger.info(f"////////////\n")
        
        logger.info(f"==============================================================\n")

        return {"query":query, "action":action, "observation": observation, "generate":response, "log": self.log_list}
