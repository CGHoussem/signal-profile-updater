import subprocess
import time
import logging
from datetime import datetime

logging.basicConfig(filename="data/log.txt")
logging.info(f"{datetime.now()}")

subprocess.run([
    'python',
    'gen_profile_pic.py'
])

time.sleep(2)

subprocess.run([
    'python',
    'update_profile.py'
])

logging.info("----------")
