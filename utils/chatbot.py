
import streamlit as st
import google.generativeai as genai
import os

# 🔐 Configure API Key
API_KEY = st.secrets.get("GOOGLE_API_KEY")

if not API_KEY:
    st.error("❌ GOOGLE_API_KEY not found. Add it in Streamlit Secrets.")
    st.stop()

genai.configure(api_key=API_KEY)

# ✅ Use stable model
model = genai.GenerativeModel("gemini-2.5-flash")


def get_ai_response(prompt):
    try:
        system_prompt = """
You are a civic assistant helping citizens report issues.

Your job:
- Understand the issue
- Suggest a short action

STRICT FORMAT:
Issue: <one line>
Action: <one line>

Do NOT add extra text.
"""

        full_prompt = system_prompt + "\nUser: " + prompt

        response = model.generate_content(full_prompt)

        if response and hasattr(response, "text"):
            return response.text.strip()
        else:
            return "⚠️ No response generated"

    except Exception as e:
        return f"⚠️ AI Error: {str(e)}"