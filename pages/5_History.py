import streamlit as st
from utils.database import load_data

st.set_page_config(page_title="History", layout="wide")

# 🎨 STYLE
st.markdown("""
<style>
.main-title {
    font-size: 40px;
    font-weight: 800;
    color: #00F5D4;
}
.card {
    background: linear-gradient(145deg, #1a1a1a, #0d0d0d);
    padding: 20px;
    border-radius: 16px;
    margin-bottom: 15px;
    box-shadow: 0px 6px 25px rgba(0,0,0,0.5);
}
.timeline {
    border-left: 3px solid #00F5D4;
    padding-left: 20px;
}
.badge-high {
    color: red;
    font-weight: bold;
}
.badge-medium {
    color: orange;
    font-weight: bold;
}
.badge-low {
    color: #00C853;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# 🔐 Login check
if not st.session_state.get("logged_in"):
    st.warning("Please login first")
    st.stop()

# 🧠 Title
st.markdown('<p class="main-title">📜 Your Complaint History</p>', unsafe_allow_html=True)
st.caption("A timeline of everything you’ve reported")

st.divider()

df = load_data()

# 👤 Filter user data
user_df = df[df["User"] == st.session_state.username]

if user_df.empty:
    st.markdown('<div class="card">📭 No complaints yet</div>', unsafe_allow_html=True)

else:
    # Sort latest first
    if "Timestamp" in user_df.columns:
        user_df = user_df.sort_values(by="Timestamp", ascending=False)

    # ==========================
    # 📊 SUMMARY
    # ==========================
    st.subheader("📊 Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total", len(user_df))

    if "Priority" in user_df.columns:
        high_count = len(user_df[user_df["Priority"] == "High"])
        col2.metric("High Priority 🔴", high_count)

    if "Category" in user_df.columns:
        most_common = user_df["Category"].mode()[0]
        col3.metric("Top Issue 📌", most_common)

    st.divider()

    # ==========================
    # 📅 TIMELINE VIEW 🔥
    # ==========================
    st.subheader("📅 Activity Timeline")

    st.markdown('<div class="timeline">', unsafe_allow_html=True)

    for _, row in user_df.iterrows():
        priority = row.get("Priority", "Low")

    # 🎯 Badge colors
    if priority == "High":
        badge_html = '<span style="color:#ff4d4d; font-weight:bold;">🔴 High</span>'
    elif priority == "Medium":
        badge_html = '<span style="color:#ffa500; font-weight:bold;">🟠 Medium</span>'
    else:
        badge_html = '<span style="color:#00c853; font-weight:bold;">🟢 Low</span>'

    # ✅ CLEAN title (NO HTML HERE)
    title = f"📌 {row.get('Category', 'Issue')}"

    with st.expander(title, expanded=False):

        st.markdown(f"""
        📍 **Location:** {row.get('Location', 'N/A')}  
        🏢 **Department:** {row.get('Department', 'N/A')}  
        📊 **Priority:** {badge_html}  
        ⏱ **Time:** {row.get('Timestamp', 'N/A')}
        """, unsafe_allow_html=True)
    st.divider()

    # ==========================
    # 📋 TABLE (OPTIONAL VIEW)
    # ==========================
    st.subheader("📋 Detailed Table")

    display_cols = [col for col in ["Category", "Department", "Priority", "Status", "Timestamp"] if col in user_df.columns]

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.dataframe(user_df[display_cols], use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)