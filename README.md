# langbase

Python, LangChain, Supabase, HuggingFace, Kubernetes, Streamlit

## 设计思路
1. 背景信息
   1. 前端其实只是保留所有的历史信息到messages列表，然后打印列表而已
   2. messages接收的query和answer都是字符串
   3. 因此后端返回的信息也是字符串，或者经过处理的字符串
## TODOs
1. 环境配置：
   1. (ok) 改到Ubuntu上
   2. (ok) 修改requirements.txt
2. 聊天场景：
   1. (ok) 添加记忆
   2. (ok) 添加预设的Prompt
   3. 添加来源
3. 添加支持的输入类型
   1. txt
   2. 网页链接
4. 添加支持的模型
   1. HuggingFace
5. UI
   1. 添加token/金额的计数显示
   2. 修改更好看的UI
6. 向量数据存储：
   1. 改为supabase
   2. 可以选择长期存储或者临时存储
7. 部署：
   1. kubernetes

## 常用指令
1. 配置环境 `sudo pip install -r requirements.txt`
2. 本地运行 `streamlit run ./src/main.py`



原始信息是：
[
0:[
0:"hello"
1:true
]
1:[
0:"Hello! How can I assist you today?"
1:false
]
]

如何解析这个tuple，从而可以使他被下面的函数作为输入并进行相应计算

import tiktoken

def get_num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301"):
    """Returns the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo":
        print("Warning: gpt-3.5-turbo may change over time. Returning num tokens assuming gpt-3.5-turbo-0301.")
        return get_num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301")
    elif model == "gpt-4":
        print("Warning: gpt-4 may change over time. Returning num tokens assuming gpt-4-0314.")
        return get_num_tokens_from_messages(messages, model="gpt-4-0314")
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif model == "gpt-4-0314":
        tokens_per_message = 3
        tokens_per_name = 1
    else:
        raise NotImplementedError(f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens

