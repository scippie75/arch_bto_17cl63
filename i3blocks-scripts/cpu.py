#!/bin/python

import subprocess
import sys

uptime = subprocess.run(['uptime'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout.split(' ')
loadavg = float(''.join(uptime[11:]).split(',')[0])

cpupower = subprocess.run(['cpupower', 'frequency-info'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout.split('\n')
freq = '?'
minfreq = 0.01
maxfreq = 1000.0
for s in cpupower:
  if 'hardware limits: ' in s:
    v = s.split(' ')
    minfreq = float(v[4]) if v[5][0] == 'G' else float(v[4]) / 1000.0
    maxfreq = float(v[7]) if v[8][0] == 'G' else float(v[7]) / 1000.0
  elif 'current policy: frequency' in s:
    v = s.split(' ')
    freq = float(v[11]) if v[12][0] == 'G' else float(v[11]) / 1000.0

cpupower_set = ''
if len(sys.argv) > 1:
  setfreq = None
  if sys.argv[1] == '1':
    if freq < maxfreq:
      setfreq = maxfreq
    else:
      setfreq = minfreq
  elif sys.argv[1] == '5':
    setfreq = freq - 0.5
  elif sys.argv[1] == '4':
    setfreq = freq + 0.5
  if setfreq:
    cpupower_set = subprocess.run(['sudo', 'cpupower', 'frequency-set', '-u', '%.1fGhz' %(setfreq)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout

print("%.2f %.1fGhz" %(loadavg, freq))

