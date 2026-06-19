from backend import chatbot
from langchain_core.messages import HumanMessage

config = {"configurable": {"thread_id": "test-1"}}

response = chatbot.invoke(
    {"messages": [HumanMessage(content="My hemoglobin is 11.2 and fasting sugar is 130, can you check my report?")]},
    config=config
)

print(response["messages"][-1].content)
#for msg in response["messages"]:
#   print(type(msg).__name__, "→", msg.content)