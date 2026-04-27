from test1 import en, den
import os

DATA_FILE = "passwd.txt"
MASTER_PASSWORD = "secret"


def verify_master(master):
    return master == MASTER_PASSWORD


def save_data(website, password, notes):
    record = f"website:{website}|password:{password}|notes:{notes}"
    encoded = en(record)

    with open(DATA_FILE, "a") as file:
        file.write(encoded + "\n")


def load_data():
    if not os.path.exists(DATA_FILE):
        return []

    records = []

    with open(DATA_FILE, "r") as file:
        for line in file:
            encoded = line.strip()
            if not encoded:
                continue

            decoded = den(encoded)
            parts = {"website": "", "password": "", "notes": ""}

            for item in decoded.split("|"):
                if ":" not in item:
                    continue
                key, value = item.split(":", 1)
                if key in parts:
                    parts[key] = value

            records.append(parts)

    return records
