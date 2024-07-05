import subprocess
try:    process = subprocess.Popen("fbwg.exe")
except FileNotFoundError:   process = subprocess.Popen(["python.exe", "fbwg.pyw"])