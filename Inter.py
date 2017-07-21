import RPi.GPIO as GPIO
import os
import R2
import Stack
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
while True:
    input_state = GPIO.input(18)
    input_state2 = GPIO.input(17)
    if input_state == False:
        os.system('R2.py')
    if input_state2== False:
        os.system('Stack.py')

