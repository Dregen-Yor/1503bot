from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from pydantic import SecretStr

deep_seek_model = ChatOpenAI(
    model="deepseek-r1",
    api_key="sk-fdbbf67d86fd4a78831d5b950ff34896",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_openai_functions_agent


class ChatAgent:
    def __init__(self, model,memory=None,system_prompt=None):
        self.model = model
        if memory is None:
            self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        else:
            self.memory = memory
        if system_prompt is not None:
            self.system_prompt = system_prompt
        else:
            self.system_prompt = "You are a helpful assistant."
        self.prompt = ChatPromptTemplate.from_messages(
        [
            ("system", self.system_prompt),
            MessagesPlaceholder(variable_name="chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )
        self.agent = create_openai_functions_agent(
            llm=self.model,
            prompt=self.prompt,
            tools=[]
        )
        self.agent_executor = AgentExecutor(agent=self.agent, tools=[], verbose=True, memory=self.memory)

    def get_system_prompt(self):
        return self.system_prompt

    def set_system_prompt(self, system_prompt):
        self.system_prompt = system_prompt

    def chat(self, messages):
        print(messages)
        return self.agent_executor.invoke({"input": messages}).get("output","抱歉，处理时遇到问题，请重试。")
    
