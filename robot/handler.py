#libraries
import sys
import RPi.GPIO as GPIO
import LCD1602
import networking
import time

from multiprocessing import Process

from apscheduler.scheduler import Scheduler
# import asyncmsg

left_wheel_pins = [6,13,19,26] #constants for wheel1
right_wheel_pins= [4,17,27,22] #constants for wheel2
sensor_echo = 20
sensor_trig = 21

step_delay = 3.0 / 1000 ##delay for step

step_count = 8

sched = Scheduler()

wheel_sequence = [[1,0,0,1], #sequence for wheels
       [1,0,0,0],
       [1,1,0,0],
       [0,1,0,0],
       [0,1,1,0],
       [0,0,1,0],
       [0,0,1,1],
       [0,0,0,1]]


def configure_io():
    outputs = left_wheel_pins + right_wheel_pins + [sensor_trig]
    print("configuring outputs %s" % outputs)
    GPIO.setmode(GPIO.BCM)
    for pin in outputs:
        GPIO.setup(pin,GPIO.OUT)
        GPIO.output(pin,False)
    print("configuring inputs for sensor" )
    #GPIO.setup(sensor_trig, GPIO.OUT)
    GPIO.setup(sensor_echo, GPIO.IN)
	

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
    outputs = left_wheel_pins + right_wheel_pins + [sensor_trig]
    GPIO.output(tuple(outputs),False)
    return read_sensors()


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


def read_sensors():
    return {"distance":distance()}

def distance():
	GPIO.output(sensor_trig, 0)
	time.sleep(0.000002)

	GPIO.output(sensor_trig, 1)
	time.sleep(0.00001)
	GPIO.output(sensor_trig, 0)

	
	while GPIO.input(sensor_echo) == 0:
		a = 0
	time1 = time.time()
	while GPIO.input(sensor_echo) == 1:
		a = 1
	time2 = time.time()

	during = time2 - time1
	return during * 340 / 2 * 100

def setStep(pinList, status):
    GPIO.output(pinList, status)


def setup():
    print ("creating new matrbot facade")
    configure_io()
    print ("showing message:")
    LCD1602.init(0x27, 1)
    LCD1602.write(0,0,"Hello im MATRBOT")
    LCD1602.write(0,1,"IP : no ip yet!")
    #p = Process(target=updateIp)
    p.start()
    asyncmsg.setup()
    configureScheduler()

def updateIp():
    count = 0
    while True:
        try:
		current_ip = networking.get_ip_address("wlan0")
        	if current_ip is None or current_ip == "" :
            		LCD1602.write(0, 1, "IP:no ip yet!"+count)
			count +=1
        	else:
            		LCD1602.write(0, 1, "IP:"+current_ip)
			break
        except:
		print("error getting ip ,retrying in 5 seconds")
		pass	
	time.sleep(5)
    print ("ip scan process finished")
	

p = Process(target=updateIp)

def configureScheduler():
    
    sched.start()
    print ("starting scheduler")
    
    sched.add_interval_job(read_sensor_state,seconds(10))
    
    

def terminate():
   print ("terminating matrbot interface")
   LCD1602.clear()
   GPIO.cleanup()
   p.terminate()
   p.join()
   sched.shutdown();
   print ("bye!")
