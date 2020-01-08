#!/usr/bin/python

import sys
import subprocess
import time, datetime

# Battery 0: Full, 100%
# Battery 0: Discharging, 96%, rate information unavailable
# Battery 0: Charging, 89%, 00:14:15 until charged
battery = subprocess.run(['acpi', '-b'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout.split('\n')

b = battery[0].split(':', 1)[1].split(',')
status = b[0].strip()
percentage = b[1].strip()
info = b[2].strip() if len(b) > 2 else ""
val = int(percentage.strip('%'))

labels = [ "", "", "", "", "" ]
label = ""
msg = ""
if status == "Discharging" or status == "Unknown":
  label = labels[0]
  if status == "Discharging":
    msg = "DIS"
  if val >= 95:
    label = labels[4]
  elif val >= 75:
    label = labels[3]
  elif val >= 50:
    label = labels[2]
  elif val >= 25:
    label = labels[1]
  else:
    label = labels[0]
elif status == "Charging":
  time = round(time.mktime(datetime.datetime.today().timetuple())) % 5
  label = labels[time % 5]
  msg = "CHR (%s)" %(info[0:5])
else:
  label = labels[4]

print("%s %s %s" %(label, percentage, msg))
print("%s %s %s" %(label, percentage, msg))

if val < 20:
  print("#FF0000")
elif val < 40:
  print("#FFAE00")
elif val < 60:
  print("#FFF600")
elif val < 85:
  print("#A8FF00")

if val < 15:
  sys.exit(33)
sys.exit(0)
