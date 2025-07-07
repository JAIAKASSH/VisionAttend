import schedule
import time
from datetime import datetime
from report_generator import generate_report
from send_whatsapp import send_whatsapp_message


def job():
    today = datetime.now().strftime("%Y-%m-%d")
    file_path = f"attendance_logs/{today}.xlsx"
    generate_report(file_path)
    
    with open(file_path, "rb") as f:
        content = f"*Attendance Report - {today}*\n(See attached report)"
        send_whatsapp_message(content)

schedule.every().day.at("18:00").do(job)

print("[SCHEDULER] Running daily task scheduler...")
while True:
    schedule.run_pending()
    time.sleep(60)
