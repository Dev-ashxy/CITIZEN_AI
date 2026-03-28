import streamlit as st
from utils.auth import login, register

st.set_page_config(page_title="CitizenAI", layout="wide")

# 🌈 Styling (SAFE)
st.markdown("""
<style>
.main-title {
    font-size: 56px;
    font-weight: 800;
    text-align: center;
    color: #4CAF50;
}
.sub-text {
    text-align: center;
    color: gray;
    margin-bottom: 30px;
}
.box {
    background: linear-gradient(145deg, #1e1e1e, #111);
    padding: 30px;
    border-radius: 16px;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.4);
}
</style>
""", unsafe_allow_html=True)

# 🏙️ Header
st.markdown('<p class="main-title">🔐 CitizenAI</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-text">Login or Register to continue</p>', unsafe_allow_html=True)

st.divider()

# 📐 Centered layout
col1, col2, col3 = st.columns([1,2,1])

with col2:
    st.markdown('<div class="box">', unsafe_allow_html=True)

    st.subheader("👤 Account Access")

    menu = st.radio("Select", ["Login", "Register"], horizontal=True)

    username = st.text_input("👤 Username")
    password = st.text_input("🔑 Password", type="password")

    st.divider()

    # ============================
    # 🔑 LOGIN (UNCHANGED LOGIC)
    # ============================
    if menu == "Login":
        if st.button("🚀 Login"):
            if not username or not password:
                st.warning("Please enter username and password")
            elif login(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username

                st.success("Login successful 🚀")

                # 🔥 Redirect
                st.switch_page("pages/4_Dashboard.py")
            else:
                st.error("Invalid credentials ❌")

    # ============================
    # 📝 REGISTER (UNCHANGED LOGIC)
    # ============================
    else:
        if st.button("✨ Register"):
            if not username or not password:
                st.warning("Please enter username and password")
            elif register(username, password):
                st.success("Registered successfully 🎉")
            else:
                st.error("User already exists ❌")

    st.markdown('</div>', unsafe_allow_html=True)