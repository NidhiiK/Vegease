from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import os

def run_main_script():
    os.system("python main.py")

scheduler = BlockingScheduler()

# Schedule the main script to run every hour
scheduler.add_job(run_main_script, 'interval', hours=1, next_run_time=datetime.now())

scheduler.start()

