#!/usr/bin/env python3

import os
import glob
import time
import RPi.GPIO as GPIO

# Activate the DS1820 module
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
# our file name 28-00000ce54ab6
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

# Typical reading (raw file)
# crc=cyclic redundancy check
# 73 01 4b 46 7f ff 0d 10 41 : crc=41 YES
# 73 01 4b 46 7f ff 0d 10 41 t=23187

def read_temp_raw():
    # Open device file and read lines, then return information
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    # Get information from module
    lines = read_temp_raw()

    #print(lines)
    # Test again if crc error
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    
    equals_pos = lines[1].find('t=')
    # Check if we have a temp and divide by 1000 and return the temperature
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c
	
def led(state='off'):
    # Set pin mode to BCM board
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    # Setup pin 17 initial to 0V
    GPIO.setup(17, GPIO.OUT, initial=GPIO.LOW)
    # If stan is on, turn on LED
    if state == 'on':
        GPIO.output(17, GPIO.HIGH)
    # Else turn off LED and cleanup
    else:
        GPIO.output(17, GPIO.LOW)
        GPIO.cleanup()

try:
    while True:
        time.sleep(1)
        temp = (read_temp())
    
        if temp >= 24:
            # Activate LED
            led(state='on')
            print(temp, 'led on')
        else:
            # Turn off LED
            led()
            print(temp, 'led off')
    
except KeyboardInterrupt:
    # Make sure led is off        
    led()
