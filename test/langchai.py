from langchain_community.chat_models import ChatZhipuAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 使用智谱
llm = ChatZhipuAI(
    model='glm-4-flash',
    api_key='04bf466f0b21cc1f81f93c8b41c25203.w3UbzllctSf97jpZ',
    temperature=0.5,
    streaming=False
)

# 创建一个提示模板
template = "Translate the following English text to Chinese: {text}"
prompt = PromptTemplate(input_variables=["text"], template=template)

# 创建一个链条
chain = prompt | llm | StrOutputParser()

# 输入文本
input_text = "Hello, how are you?"

# 生成响应
def test():
    response = chain.invoke({"text": input_text})
    print(response)