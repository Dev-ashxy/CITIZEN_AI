import streamlit as st

# Page config
st.set_page_config(page_title="CitizenAI", layout="wide")

# Session state init
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# 🌈 Custom styling (SAFE)
st.markdown("""
<style>
.main-title {
    font-size: 48px;
    font-weight: bold;
    color: #4CAF50;
    text-align: center;
}
.sub-text {
    text-align: center;
    font-size: 18px;
    color: gray;
}
.card {
    background-color: #111;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# 🏙️ Title
st.markdown('<p class="main-title"> CitizenAI</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-text">AI-powered Civic Issue Reporting System</p>', unsafe_allow_html=True)

st.divider()

# 📊 Layout
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="card">📸<br><br>Upload Issues</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">🤖<br><br>AI Detection</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="card">📊<br><br>Track Complaints</div>', unsafe_allow_html=True)

st.divider()

# 🔐 Login Status
if st.session_state.logged_in:
    st.success(f"✅ Welcome, {st.session_state.username}!")
else:
    st.warning("⚠️ Please login from Home page")

# 📌 Footer
st.markdown("""
---
<center>🚀 Built with Streamlit | CitizenAI Project</center>
""", unsafe_allow_html=True)