import os
import pandas as pd
from datetime import datetime

ATTENDANCE_DIR = "attendance_logs"

def log_attendance(name):
    os.makedirs(ATTENDANCE_DIR, exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")
    file_path = os.path.join(ATTENDANCE_DIR, f"{date_str}.xlsx")

    time_str = datetime.now().strftime("%H:%M:%S")
    new_entry = pd.DataFrame([[name, date_str, time_str]], columns=["Name", "Date", "Time"])

    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
        if not ((df["Name"] == name) & (df["Date"] == date_str)).any():
            df = pd.concat([df, new_entry], ignore_index=True)
            df.to_excel(file_path, index=False)
    else:
        new_entry.to_excel(file_path, index=False)

    print(f"[LOGGED] {name} at {time_str}")
