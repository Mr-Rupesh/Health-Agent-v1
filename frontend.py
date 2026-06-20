import streamlit as st
from backend import chatbot
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
import uuid

# =========================== Utilities ===========================
def generate_thread_id():
    return uuid.uuid4()

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state["thread_id"] = thread_id
    add_thread(thread_id)
    st.session_state["message_history"] = []

def add_thread(thread_id):
    if thread_id not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(thread_id)

def load_conversation(thread_id):
    state = chatbot.get_state(config={"configurable": {"thread_id": thread_id}})
    return state.values.get("messages", [])

# ======================= Session Initialization ===================
if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_thread_id()

if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = []

add_thread(st.session_state["thread_id"])

st.set_page_config(page_title="MediGuide", page_icon="🏥")

# ============================ Sidebar ============================
st.sidebar.title("MediGuide")
st.sidebar.caption("AI Health Assistant — for informational purposes only, not medical advice.")

if st.sidebar.button("New Conversation"):
    reset_chat()

st.sidebar.markdown("---")
st.sidebar.subheader("Lab Report Values (optional)")

with st.sidebar.form("lab_form"):
    hemoglobin = st.number_input("Hemoglobin (g/dL)", min_value=0.0, value=0.0, step=0.1)
    fasting_sugar = st.number_input("Fasting Sugar (mg/dL)", min_value=0.0, value=0.0, step=1.0)
    bp_systolic = st.number_input("BP Systolic (mmHg)", min_value=0.0, value=0.0, step=1.0)
    bp_diastolic = st.number_input("BP Diastolic (mmHg)", min_value=0.0, value=0.0, step=1.0)
    cholesterol = st.number_input("Cholesterol (mg/dL)", min_value=0.0, value=0.0, step=1.0)
    creatinine = st.number_input("Creatinine (mg/dL)", min_value=0.0, value=0.0, step=0.1)
    wbc_count = st.number_input("WBC Count (cells/µL)", min_value=0.0, value=0.0, step=100.0)

    submitted = st.form_submit_button("Analyze Report")

st.sidebar.markdown("---")
st.sidebar.subheader("Conversations")
for thread_id in st.session_state["chat_threads"][::-1]:
    if st.sidebar.button(str(thread_id)[:8]):
        st.session_state["thread_id"] = thread_id
        messages = load_conversation(thread_id)
        temp_messages = []
        for msg in messages:
            if isinstance(msg, (HumanMessage, AIMessage)):
                role = "user" if isinstance(msg, HumanMessage) else "assistant"
                if isinstance(msg.content, list):
                    content = msg.content[0].get("text", "") if msg.content else ""
                else:
                    content = msg.content
                temp_messages.append({"role": role, "content": content})
        st.session_state["message_history"] = temp_messages

# ============================ Main UI ============================
st.title("MediGuide — AI Health Assistant")
st.info("⚠️ This tool is for informational purposes only. Always consult a qualified doctor.")

CONFIG = {
    "configurable": {"thread_id": st.session_state["thread_id"]},
    "metadata": {"thread_id": st.session_state["thread_id"]},
    "run_name": "chat_turn",
}

def send_message(user_input):
    st.session_state["message_history"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.text(user_input)

    with st.chat_message("assistant"):
        status_holder = {"box": None}

        def ai_only_stream():
            for message_chunk, metadata in chatbot.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode="messages",
            ):
                if isinstance(message_chunk, ToolMessage):
                    tool_name = getattr(message_chunk, "name", "tool")
                    if status_holder["box"] is None:
                        status_holder["box"] = st.status(f"🔧 Using `{tool_name}` …", expanded=True)
                    else:
                        status_holder["box"].update(label=f"🔧 Using `{tool_name}` …", state="running", expanded=True)

                if isinstance(message_chunk, AIMessage):
                    if message_chunk.content:
                        text = message_chunk.content[0].get("text", "") if isinstance(message_chunk.content, list) else message_chunk.content
                        if text:
                            yield text

        ai_message = st.write_stream(ai_only_stream())

        if status_holder["box"] is not None:
            status_holder["box"].update(label="✅ Done", state="complete", expanded=False)

    st.session_state["message_history"].append({"role": "assistant", "content": ai_message})

# Render chat history
for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):
        st.text(message["content"])

# Handle lab form submission
if submitted:
    values = {
        "hemoglobin": hemoglobin,
        "fasting_sugar": fasting_sugar,
        "bp_systolic": bp_systolic,
        "bp_diastolic": bp_diastolic,
        "cholesterol": cholesterol,
        "creatinine": creatinine,
        "wbc_count": wbc_count,
    }
    filled_values = {k: v for k, v in values.items() if v > 0}
    if filled_values:
        report_text = "Please analyze my lab report: " + ", ".join(
            [f"{k} = {v}" for k, v in filled_values.items()]
        )
        send_message(report_text)
    else:
        st.sidebar.warning("Enter at least one value before submitting.")

# Handle chat input
user_input = st.chat_input("Describe your symptoms or ask a question...")
if user_input:
    send_message(user_input)