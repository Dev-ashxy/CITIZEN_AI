import streamlit as st
from utils.chatbot import get_ai_response

st.set_page_config(page_title="AI Assistant", layout="wide")

# 🎨 Styling
st.markdown("""
<style>
.title {
    font-size: 40px;
    font-weight: 800;
    color: #00C9A7;
}
.chat-container {
    background: linear-gradient(145deg, #1e1e1e, #111);
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.4);
}
</style>
""", unsafe_allow_html=True)

# 🔐 Login check (UNCHANGED)
if not st.session_state.get("logged_in"):
    st.warning("🔒 Please login first")
    st.stop()

# 🧠 Header
st.markdown('<p class="title">🤖 AI Civic Assistant</p>', unsafe_allow_html=True)
st.caption("Describe your issue and get instant guidance")

st.divider()

# 💬 Chat memory (UNCHANGED)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 📦 Chat container
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# 📜 Show previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

st.markdown('</div>', unsafe_allow_html=True)

# 💬 Input
user_input = st.chat_input("💭 Describe your issue...")

if user_input:
    # 🧑 Show user message
    with st.chat_message("user"):
        st.markdown(user_input)

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # 🤖 AI Thinking Spinner
    with st.spinner("🤖 AI is thinking..."):
        reply = get_ai_response(user_input)

    # ✨ Typing effect
    with st.chat_message("assistant"):
        placeholder = st.empty()
        msg = ""
        for ch in reply:
            msg += ch
            placeholder.markdown(msg)

    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })

# 🚀 Smart Action Button (UNCHANGED LOGIC)
if "messages" in st.session_state and len(st.session_state.messages) > 0:
    last_msg = st.session_state.messages[-1]["content"].lower()

    if "issue" in last_msg or "problem" in last_msg:
        st.success("👉 You can now report this issue")

        if st.button("🚀 Go to Report Issue"):
            st.switch_page("pages/2_Report_Issue.py")