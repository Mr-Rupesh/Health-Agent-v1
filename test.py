from backend import chatbot
from langchain_core.messages import HumanMessage

config = {"configurable": {"thread_id": "test-1"}}

response = chatbot.invoke(
    {"messages": [HumanMessage(content="My weight is 70kg and height is 175cm, what is my BMI?")]},
    config=config
)

for msg in response["messages"]:
    print(type(msg).__name__, "→", msg.content)