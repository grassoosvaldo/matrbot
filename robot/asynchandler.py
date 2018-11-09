 
import sys
import RPi.GPIO as GPIO
import time
import status

left_wheel_pins = [6,13,19,26] #constants for wheel1
right_wheel_pins= [4,17,27,22] #constants for wheel2
step_delay = 3.0 / 1000 ##delay for step

step_count = 8
wheel_sequence = [[1,0,0,1], #sequence for wheels
       [1,0,0,0],
       [1,1,0,0],
       [0,1,0,0],
       [0,1,1,0],
       [0,0,1,0],
       [0,0,1,1],
       [0,0,0,1]]

def configure_io():
    outputs = left_wheel_pins + right_wheel_pins
    print "configuring outputs %s" % outputs
    GPIO.setmode(GPIO.BCM)
    for pin in outputs:
        GPIO.setup(pin,GPIO.OUT)
        GPIO.output(pin,False)
    print "configuring inputs for sensor"
    #GPIO.setup(sensor_trig, GPIO.OUT)
    #GPIO.setup(sensor_echo, GPIO.IN)
    
def handle_wheels(direction = None):
    if direction['side'] == "forward":
        walkForward(direction['steps'])
    elif direction['side'] == "backwards":
        walkBackwards(direction['steps'])
    elif direction['side'] == "left":
        turnLeft(direction['steps'])
    elif direction['side'] == "right":
        turnRight(direction['steps'])
    #reset status
    outputs = left_wheel_pins + right_wheel_pins
    GPIO.output(tuple(outputs),False)
    #return read_sensors()
    
def walkForward(steps=None):
    for i in range(steps):
        for j in range(step_count):
            rWheel = wheel_sequence[j]
            lWheel = list(reversed(wheel_sequence[j]))
            setStep(tuple(left_wheel_pins+right_wheel_pins),tuple(rWheel+lWheel))
            time.sleep(step_delay)


def walkBackwards(steps=None):
    for i in range(steps):
        for j in range(step_count):
            rWheel = list(reversed(wheel_sequence[j]))
            lWheel = wheel_sequence[j]
            setStep(tuple(left_wheel_pins+right_wheel_pins),tuple(rWheel+lWheel))
            time.sleep(step_delay)


def turnLeft(steps=None):
    for i in range(steps):
        for j in range(step_count):
            rWheel = wheel_sequence[j]
            lWheel = wheel_sequence[j]
            setStep(tuple(left_wheel_pins+right_wheel_pins),tuple(rWheel+lWheel))
            time.sleep(step_delay)


def turnRight(steps=None):
    for i in range(steps):
        for j in range(step_count):
            rWheel = list(reversed(wheel_sequence[j]))
            #lWheel = reversed(wheel_sequence[j])
            lWheel = rWheel
            setStep(tuple(left_wheel_pins+right_wheel_pins),tuple(rWheel+lWheel))
            time.sleep(step_delay)
            
def setStep(pinList, status):
    GPIO.output(pinList, status)
            
def read_sensors():
    return status(distance=100, hit=False)


def terminate():
   print "terminating matrbot interface"
   GPIO.cleanup()
