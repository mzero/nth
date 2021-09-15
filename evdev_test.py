#!/usr/bin/env python

import liblo, sys 
from evdev import InputDevice, categorize, ecodes
from select import select
 
#devices = ( evdev.InputDevice('/dev/input/event9'),evdev.InputDevice('/dev/input/event8'),evdev.InputDevice('/dev/input/event7'),evdev.InputDevice('/dev/input/event10'))
devices = map(InputDevice, ('/dev/input/event9', '/dev/input/event8', '/dev/input/event7', '/dev/input/event10', '/dev/input/event5', '/dev/input/event11'))
devices = {dev.fd: dev for dev in devices}

for dev in devices.values(): print(dev)

position = [0,0,0,0,0]
key = 0

# send all messages to port 4000 on the local machine
try:
    target = liblo.Address(4000)
except liblo.AddressError, err:
    print str(err)
    sys.exit()

while True:
    r, w, x = select(devices, [], [])
    for fd in r:
        for event in devices[fd].read():

            if event.type == ecodes.EV_KEY:
                #print(categorize(event))
                key = event.value
                
            if event.type == ecodes.EV_REL:
                #print(devices[fd].name)
                #print('value: {}'.format(event.value))
                
                # constrain a value to be 0-255
                #outval = min(max(val, 0), 1023)
                
                if (devices[fd].name == "soc:knob1"):
                    position[0] += event.value * 5
                    position[0] = min(max(position[0], 0), 1023)
                    liblo.send(target, "/knobs/1", position[0])
                if (devices[fd].name == "soc:knob2"):
                    position[1] += event.value * 5
                    position[1] = min(max(position[1], 0), 1023)
                    liblo.send(target, "/knobs/2", position[1])
                if (devices[fd].name == "soc:knob3"):
                    position[2] += event.value * 5
                    position[2] = min(max(position[2], 0), 1023)
                    liblo.send(target, "/knobs/3", position[2])
                if (devices[fd].name == "soc:knob4"):
                    position[3] += event.value * 5
                    position[3] = min(max(position[3], 0), 1023)
                    liblo.send(target, "/knobs/4", position[3])
                    
            if event.type == ecodes.EV_ABS:
                #print(event)
                #print(categorize(event))
                if (devices[fd].name == "raspberrypi-ts"):
                    if event.code == ecodes.ABS_X:
                        position[4] = event.value * 1.28
                        position[4] = min(max(position[4], 0), 1023)
                        liblo.send(target, "/knobs/5", position[4])