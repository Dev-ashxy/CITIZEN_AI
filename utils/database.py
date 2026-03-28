import pandas as pd
import os

FILE = os.path.join("data", "complaints.csv")

COLUMNS = [
    "ID", "User", "Category", "Confidence",
    "Department", "Priority", "Location",
    "Status", "Timestamp"
]

def load_data():
    os.makedirs("data", exist_ok=True)

    # If file doesn't exist → create it
    if not os.path.exists(FILE):
        df = pd.DataFrame(columns=COLUMNS)
        df.to_csv(FILE, index=False)
        return df

    # If file exists but is empty → fix it
    if os.path.getsize(FILE) == 0:
        df = pd.DataFrame(columns=COLUMNS)
        df.to_csv(FILE, index=False)
        return df

    try:
        df = pd.read_csv(FILE)

        # If columns missing → reset file
        if df.empty or list(df.columns) != COLUMNS:
            df = pd.DataFrame(columns=COLUMNS)
            df.to_csv(FILE, index=False)

        return df

    except:
        # If corrupted → reset safely
        df = pd.DataFrame(columns=COLUMNS)
        df.to_csv(FILE, index=False)
        return df


def save_data(new_entry):
    df = load_data()
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv(FILE, index=False)