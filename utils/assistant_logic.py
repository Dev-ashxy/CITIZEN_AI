from utils.logic import get_department, get_priority


def generate_response(user_input):
    text = user_input.lower()

    # 🔍 Keyword mapping
    if any(word in text for word in ["road", "pothole", "street", "damage"]):
        category = "Road Issue"

    elif any(word in text for word in ["water", "flood", "leak", "drain"]):
        category = "Water"

    elif any(word in text for word in ["electric", "wire", "pole", "shock", "cable"]):
        category = "Electricity"

    elif any(word in text for word in ["garbage", "waste", "trash", "dustbin"]):
        category = "Sanitation"

    elif any(word in text for word in ["fire", "smoke", "burn", "flame"]):
        category = "Fire Hazard"

    else:
        return "⚠️ I couldn't understand the issue. Please describe it clearly."

    # 🎯 Get department + priority
    department = get_department(category)
    priority, severity = get_priority(category)

    # 💬 Final smart response
    return f"""
🚨 Issue Detected: {category}

🏢 Department: {department}  
⚡ Priority: {priority} ({severity})

👉 Please use the 'Report Issue' section to submit this complaint.
"""