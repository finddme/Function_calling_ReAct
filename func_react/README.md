# Function_calling_ReAct

- Function calling을 적용하여 [#ReACT #HITL #Multi-Agent post](https://finddme.github.io/dev%20log/2024/08/08/react_agent/)를 구현한 프로젝트.
- **Model** openai, Claude, Groq, Together ai 선택 가능 (현 blog search box는 Together ai LLaMa 3.1 70B 적용)
- Finance action 추가 (해당 기능 개선 중)

```
func_react
├── action_agents
│   ├── actions.py
│   ├── __init__.py
│   └── search_engine.py
├── app
│   ├── app.py
│   ├── __init__.py
│   └── streamlit.py
├── blog_search_box
│   ├── .devcontainer
│   │   └── devcontainer.json
│   ├── README.md
│   ├── .streamlit
│   │   └── config.toml
│   └── streamlit.py
├── db
│   ├── data_processing.py
│   ├── db_management.py
│   ├── __init__.py
│   └── retrieve.py
├── graph
│   ├── graph.py
│   ├── __init__.py
│   └── node.py
├── main.py
├── model
│   ├── completion.py
│   ├── function_calling.py
│   ├── functions.py
│   ├── __init__.py
│   ├── model_prep.py
│   ├── models.py
│   ├── processor.py
│   ├── prompt.py
│   └── setting.py
├── README.md
└── utils
    ├── config.py
    ├── formats.py
    ├── __init__.py
    ├── logger.py
    ├── logging_wrapper.py
    └── map.py
```

## Pipeline 

<center><img width="1000" src="https://github.com/user-attachments/assets/336fe90a-a8d4-4244-a213-7f74558f5100"></center>
<center><em style="color:gray;">Illustrated by the author</em></center><br>
