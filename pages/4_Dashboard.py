import streamlit as st
from utils.database import load_data

st.set_page_config(page_title="Dashboard", layout="wide")

# 🎨 ULTRA UI STYLE
st.markdown("""
<style>
.main-title {
    font-size: 44px;
    font-weight: 900;
    color: #00F5D4;
}
.card {
    background: linear-gradient(145deg, #1a1a1a, #0d0d0d);
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0px 6px 25px rgba(0,0,0,0.5);
}
.metric-card {
    background: linear-gradient(145deg, #222, #111);
    padding: 18px;
    border-radius: 14px;
    text-align: center;
    transition: 0.3s;
}
.metric-card:hover {
    transform: scale(1.05);
}
.section-title {
    font-size: 24px;
    font-weight: 700;
    margin-top: 25px;
}
</style>
""", unsafe_allow_html=True)

# 🔐 Login check
if not st.session_state.get("logged_in"):
    st.warning("Please login first")
    st.stop()

# 🧠 HEADER
st.markdown('<p class="main-title">🚀 CitizenAI Command Center</p>', unsafe_allow_html=True)
st.caption("Monitor, analyze and control civic intelligence in real-time")

st.divider()

df = load_data()

# 🚫 EMPTY STATE
if df.empty:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.info("🚫 No complaints yet. Start reporting issues to activate the system.")
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # ==========================
    # 📊 METRICS + MINI INSIGHT
    # ==========================
    st.markdown('<p class="section-title">📊 Live Overview</p>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    total = len(df)
    high = len(df[df["Priority"] == "High"]) if "Priority" in df.columns else 0
    pending = len(df[df["Status"] == "Pending"]) if "Status" in df.columns else 0
    resolved = len(df[df["Status"] == "Resolved"]) if "Status" in df.columns else 0

    with col1:
        st.markdown(f'<div class="metric-card">📦<br>Total<br><h2>{total}</h2></div>', unsafe_allow_html=True)

    with col2:
        st.markdown(f'<div class="metric-card">🔴<br>High Priority<br><h2>{high}</h2></div>', unsafe_allow_html=True)

    with col3:
        st.markdown(f'<div class="metric-card">⏳<br>Pending<br><h2>{pending}</h2></div>', unsafe_allow_html=True)

    with col4:
        st.markdown(f'<div class="metric-card">✅<br>Resolved<br><h2>{resolved}</h2></div>', unsafe_allow_html=True)

    # 🧠 Smart Insight (NEW but no logic change)
    if total > 0:
        st.success(f"📢 {round((resolved/total)*100)}% issues resolved so far!")

    st.divider()

    # ==========================
    # 🔍 FILTER BAR (NEW UI ONLY)
    # ==========================
    st.markdown('<p class="section-title">🔍 Filters</p>', unsafe_allow_html=True)

    f1, f2 = st.columns(2)

    with f1:
        category_filter = st.selectbox(
            "Filter by Category",
            ["All"] + list(df["Category"].unique()) if "Category" in df.columns else ["All"]
        )

    with f2:
        status_filter = st.selectbox(
            "Filter by Status",
            ["All"] + list(df["Status"].unique()) if "Status" in df.columns else ["All"]
        )

    # Apply filters (UI layer only)
    filtered_df = df.copy()

    if category_filter != "All":
        filtered_df = filtered_df[filtered_df["Category"] == category_filter]

    if status_filter != "All":
        filtered_df = filtered_df[filtered_df["Status"] == status_filter]

    st.divider()

    # ==========================
    # 📊 CHARTS
    # ==========================
    colA, colB = st.columns(2)

    with colA:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📌 Issues by Category")
        if "Category" in filtered_df.columns:
            st.bar_chart(filtered_df["Category"].value_counts())
        st.markdown('</div>', unsafe_allow_html=True)

    with colB:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📊 Status Breakdown")
        if "Status" in filtered_df.columns:
            st.bar_chart(filtered_df["Status"].value_counts())
        st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    # ==========================
    # 📈 TREND (NEW 🔥)
    # ==========================
    st.markdown('<p class="section-title">📈 Complaint Trend</p>', unsafe_allow_html=True)

    if "Timestamp" in filtered_df.columns:
        try:
            temp_df = filtered_df.copy()
            temp_df["Timestamp"] = temp_df["Timestamp"].str[:10]
            trend = temp_df["Timestamp"].value_counts().sort_index()
            st.line_chart(trend)
        except:
            st.warning("Could not generate trend chart")

    st.divider()

    # ==========================
    # 📋 TABLE
    # ==========================
    st.markdown('<p class="section-title">🧾 Recent Complaints</p>', unsafe_allow_html=True)

    if "Timestamp" in filtered_df.columns:
        filtered_df = filtered_df.sort_values(by="Timestamp", ascending=False)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.dataframe(filtered_df.head(10), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)