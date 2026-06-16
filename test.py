from backend import chatbot
from langchain_core.messages import HumanMessage

config = {"configurable": {"thread_id": "test-1"}}

response = chatbot.invoke(
    {"messages": [HumanMessage(content="Hello, I have a headache. What should I do?")]},
    config=config
)

print(response["messages"][-1].content)