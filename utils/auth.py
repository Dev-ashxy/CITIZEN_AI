import pandas as pd
import os
import hashlib

FILE = os.path.join("data", "users.csv")


# 🔐 Hash password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def load_users():
    if not os.path.exists(FILE) or os.path.getsize(FILE) == 0:
        os.makedirs("data", exist_ok=True)
        df = pd.DataFrame(columns=["username", "password"])
        df.to_csv(FILE, index=False)
        return df

    try:
        df = pd.read_csv(FILE)
        if "username" not in df.columns:
            raise Exception()
        return df
    except:
        df = pd.DataFrame(columns=["username", "password"])
        df.to_csv(FILE, index=False)
        return df


def register(username, password):
    df = load_users()

    username = str(username).strip().lower()
    password = str(password).strip()

    if username == "" or password == "":
        return False

    # Normalize usernames
    df["username"] = df["username"].astype(str).str.strip().str.lower()

    if username in df["username"].tolist():
        return False

    # 🔐 Hash password before saving
    hashed_password = hash_password(password)

    new_user = pd.DataFrame([{
        "username": username,
        "password": hashed_password
    }])

    df = pd.concat([df, new_user], ignore_index=True)
    df.to_csv(FILE, index=False)

    return True


def login(username, password):
    df = load_users()

    username = str(username).strip().lower()
    password = str(password).strip()

    df["username"] = df["username"].astype(str).str.strip().str.lower()
    df["password"] = df["password"].astype(str).str.strip()

    hashed_password = hash_password(password)

    user = df[
        (df["username"] == username) &
        (df["password"] == hashed_password)
    ]

    return not user.empty