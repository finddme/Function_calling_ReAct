# Function_calling_ReAct

- Function calling을 적용하여 [#ReACT #HITL #Multi-Agent post](https://finddme.github.io/dev%20log/2024/08/08/react_agent/)를 구현한 프로젝트.
- **Model** openai, Claude, Groq, Together ai 선택 가능 (현 blog search box는 Together ai LLaMa 3.1 70B 적용)
- Finance action 추가 (해당 기능 개선 중)


## func_react

- streaming 기능 X
- image generation 기능 포함

### Pipeline 

<center><img width="1000" src="https://github.com/user-attachments/assets/336fe90a-a8d4-4244-a213-7f74558f5100"></center>
<center><em style="color:gray;">Illustrated by the author</em></center><br>

### Start app

```
# api run
python main.py

# streamlit run
streamlit run streamlit.py
```

## func_react_stream

- streaming 기능 O
- image generation 기능 미포함
  
### Pipeline 

<center><img width="1000" src="https://github.com/user-attachments/assets/336fe90a-a8d4-4244-a213-7f74558f5100"></center>
<center><em style="color:gray;">Illustrated by the author</em></center><br>

### Start app

```
# api run
python main.py

# streamlit run
streamlit run streamlit.py
```
