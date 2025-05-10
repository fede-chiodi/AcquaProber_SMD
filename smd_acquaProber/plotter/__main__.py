#!/usr/bin/python3
import RPi.GPIO as GPIO
import time

in1 = 23
in2 = 24
in3 = 25
in4 = 8

# careful lowering this, at some point you run into the mechanical limitation of how quick your motor can move
step_sleep = 0.002

step_count = 4096 # 5.625*(1/64) per step, 4096 steps is 360°

direction = False # True for clockwise, False for counter-clockwise

# defining stepper motor sequence (found in documentation http://www.4tronix.co.uk/arduino/Stepper-Motors.php)
step_sequence = [[1,0,0,1],
                 [1,0,0,0],
                 [1,1,0,0],
                 [0,1,0,0],
                 [0,1,1,0],
                 [0,0,1,0],
                 [0,0,1,1],
                 [0,0,0,1]]

# setting up
GPIO.setmode( GPIO.BCM )
GPIO.setup( in1, GPIO.OUT )
GPIO.setup( in2, GPIO.OUT )
GPIO.setup( in3, GPIO.OUT )
GPIO.setup( in4, GPIO.OUT )

# initializing
GPIO.output( in1, GPIO.LOW )
GPIO.output( in2, GPIO.LOW )
GPIO.output( in3, GPIO.LOW )
GPIO.output( in4, GPIO.LOW )

motor_pins = [in1,in2,in3,in4]
motor_step_counter = 0 ;

def step(direction: bool = True):
    global motor_step_counter
    if(direction):
        motor_step_counter += 1
    elif(motor_step_counter == 0):
        motor_step_counter = 7
    else:
        motor_step_counter -= 1
    for pin in range(0, len(motor_pins)):
        GPIO.output(motor_pins[pin], step_sequence[motor_step_counter%8][pin])
    time.sleep(step_sleep)

def rotate(steps: int, direction: bool = True):
    for _ in range(steps):
        step(direction)


def clockwise():
    for _ in range(step_count):
        step(True)

def c_clockwise():
    for _ in range(step_count):
        step(False)

def cleanup():
    GPIO.output( in1, GPIO.LOW )
    GPIO.output( in2, GPIO.LOW )
    GPIO.output( in3, GPIO.LOW )
    GPIO.output( in4, GPIO.LOW )
    GPIO.cleanup()

print("Starting rotation...")
while True:
    clockwise()
    c_clockwise()
cleanup()
exit( 0 )
