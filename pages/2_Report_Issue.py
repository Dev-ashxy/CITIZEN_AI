import streamlit as st
import uuid
import datetime

from utils.database import save_data
from utils.image_ai import classify_image
from utils.logic import get_department, get_priority

st.set_page_config(page_title="Report Issue", layout="wide")

# 🎨 Custom Styling
st.markdown("""
<style>
.title {
    font-size: 42px;
    font-weight: 800;
    color: #4CAF50;
}
.card {
    background: linear-gradient(145deg, #1e1e1e, #111);
    padding: 25px;
    border-radius: 16px;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.4);
}
.section {
    font-size: 20px;
    font-weight: 600;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)

# 🔐 Login check (UNCHANGED)
if not st.session_state.get("logged_in"):
    st.stop()

# 🏙️ Header
st.markdown('<p class="title">📸 Report an Issue</p>', unsafe_allow_html=True)
st.caption("Upload an image and let AI detect the issue automatically")

st.divider()

# 📐 Layout
col1, col2 = st.columns([1, 1])

# =========================
# 📤 LEFT SIDE (INPUT)
# =========================
with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown("### 📤 Upload Details")

    image = st.file_uploader("Upload Image")
    location = st.text_input("📍 Enter Location")

    if st.button("🔍 Analyze"):
        if image and location:
            st.session_state.result = classify_image(image)
        else:
            st.warning("Please upload image and enter location")

    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# 🤖 RIGHT SIDE (RESULT)
# =========================
with col2:
    if "result" in st.session_state:
        category, confidence, note, edges = st.session_state.result

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.markdown("### 🤖 AI Analysis")

        st.success(f"**Category:** {category}")

        # 📊 Confidence Progress Bar
        st.markdown("#### 📊 Confidence Level")
        st.progress(min(int(confidence * 100), 100))
        st.caption(f"{confidence * 100:.1f}% confidence")

        st.write(note)

        if edges is not None:
            st.image(edges, caption="Edge Detection View", use_column_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

        st.divider()

        # =========================
        # 👤 USER CONFIRMATION
        # =========================
        st.markdown("### 👤 Confirm & Submit")

        options = ["Road Issue", "Sanitation", "Water", "Electricity", "Fire Hazard"]

        category_map = {
            "road": "Road Issue",
            "garbage": "Sanitation",
            "water": "Water",
            "electricity": "Electricity",
            "fire": "Fire Hazard"
        }

        default_category = category_map.get(category, "Road Issue")

        selected_category = st.selectbox(
            "Confirm Category",
            options,
            index=options.index(default_category)
        )

        # 🎯 Priority (NO LOGIC CHANGE)
        priority, priority_note = get_priority(selected_category)

        # 🎨 Color-coded priority
        if priority == "High":
            st.error(f"🔥 Priority: {priority} - {priority_note}")
        elif priority == "Medium":
            st.warning(f"⚠️ Priority: {priority} - {priority_note}")
        else:
            st.success(f"✅ Priority: {priority} - {priority_note}")

        # 🚀 Submit
        if st.button("🚀 Submit Complaint"):
            department = get_department(selected_category)

            complaint = {
                "ID": str(uuid.uuid4())[:8],
                "User": st.session_state.username,
                "Category": selected_category,
                "Confidence": confidence,
                "Department": department,
                "Priority": priority,
                "Location": location,
                "Status": "Pending",
                "Timestamp": str(datetime.datetime.now())
            }

            save_data(complaint)

            del st.session_state["result"]

            st.success("✅ Complaint Submitted Successfully!")