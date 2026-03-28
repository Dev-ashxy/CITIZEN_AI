def get_department(category):
    mapping = {
        "Road Issue": "PWD",
        "Garbage Issue": "Municipality",
        "Water Logging": "Water Department",
        "Electricity Issue": "Electric Department",
        "Fire Hazard": "Emergency Services"
    }
    return mapping.get(category, "General")


def get_priority(category):
    if category == "Fire Hazard":
        return "High", "Emergency 🚨"

    elif category == "Electricity Issue":
        return "High", "Danger ⚡"

    elif category == "Water Logging":
        return "Medium", "Flood Risk 💧"

    elif category == "Road Issue":
        return "Medium", "Public Issue 🛣️"

    elif category == "Garbage Issue":
        return "Low", "Sanitation 🗑️"

    else:
        return "Low", "Normal"