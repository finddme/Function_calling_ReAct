# Function_calling_ReAct

- Function calling을 적용하여 [#ReACT #HITL #Multi-Agent post](https://finddme.github.io/dev%20log/2024/08/08/react_agent/)를 구현한 프로젝트.
- **Model** openai, Claude, Groq, Together ai 선택 가능 (현 blog search box는 Together ai LLaMa 3.1 70B 적용)
- Finance action 추가 (해당 기능 개선 중)

```
func_react_stream
|-- action_agents
|   |-- __init__.py
|   |-- actions.py
|   `-- search_engine.py
|-- app
|   |-- __init__.py
|   |-- app.py
|   `-- streamlit.py
|-- db
|   |-- __init__.py
|   |-- data_processing.py
|   |-- db_management.py
|   `-- retrieve.py
|-- main.py
|-- model
|   |-- __init__.py
|   |-- completion.py
|   |-- function_calling.py
|   |-- functions.py
|   |-- model_prep.py
|   |-- model_prep_stream.py
|   |-- models.py
|   |-- processor.py
|   |-- prompt.py
|   `-- setting.py
|-- run
|   |-- __init__.py
|   |-- node.py
|   `-- run.py
`-- utils
    |-- __init__.py
    |-- config.py
    |-- formats.py
    |-- logger.py
    |-- logging_wrapper.py
    `-- map.py
```

## Pipeline 

<center><img width="1000" src="https://github.com/user-attachments/assets/336fe90a-a8d4-4244-a213-7f74558f5100"></center>
<center><em style="color:gray;">Illustrated by the author</em></center><br>
