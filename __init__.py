import bhi160
import display
import leds
import os
import utime

try:
    accel = bhi160.BHI160Accelerometer()
except:
    os.reset()

leds.clear()
with display.open() as d:
    d.clear()
    d.update()

for i in range(3):
    leds.set_rocket(i, 0)

charset = {
    'd': [0x7ff, 0x603, 0x30e, 0x18c],
    'f': [0x7ff, 0x063, 0x063, 0x063],
    'l': [0x7ff, 0x600, 0x600, 0x600],
    'o': [0x1fb, 0x603, 0x603, 0x1fb],
    'p': [0x7ff, 0x063, 0x03e, 0x01c],
    'y': [0x003, 0x00c, 0x7f8, 0x00c, 0x003],
    '_': [0x400] * 4,
}

string = []
for c in 'polyfloyd':
    string = string + charset[c] + [0]

while True:
    sign = lambda v: 1 if v>=0 else -1
    accel_hist = []
    direction = 0
    while direction == 0:
        samples = accel.read()
        accel_hist.extend([ 0 if abs(s.y) < 0.2 else s.y for s in samples ])
        accel_hist = accel_hist[max(len(accel_hist)-20, 0):]
        if len(accel_hist) > 2:
            direction = sign(accel_hist[-1]) - sign(accel_hist[-2])
    
    colors = [(0, 0, 0), (192, 192, 192)]
    string_iter = string
    if direction > 0:
        string_iter = reversed(string_iter)
    for column in string:
        for l in range(11):
            leds.set(10-l, colors[column>>l & 1])
    leds.clear()
    utime.sleep(0.001)
