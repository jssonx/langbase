# langbase-v1

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