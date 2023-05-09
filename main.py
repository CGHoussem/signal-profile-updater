import subprocess
import time

subprocess.run([
    'python',
    'gen_profile_pic.py'
])

time.sleep(2)

subprocess.run([
    'python',
    'update_profile.py'
])
