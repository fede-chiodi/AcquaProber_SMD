import RPi.GPIO as GPIO
from time import sleep

servo_pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

pwm = GPIO.PWM(servo_pin, 50)
pwm.start(0)

valve_open = False

def open_valve():
    global valve_open
    pwm.ChangeDutyCycle(12.5)
    sleep(1)
    pwm.ChangeDutyCycle(0)
    valve_open = True

def close_valve():
    global valve_open
    pwm.ChangeDutyCycle(2.5)
    sleep(1)
    pwm.ChangeDutyCycle(0)
    valve_open = False

def is_valve_open():
    return valve_open

def cleanup():
    pwm.stop()
    GPIO.cleanup()
