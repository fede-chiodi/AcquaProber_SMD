#!/usr/bin/python3
import RPi.GPIO as GPIO
import time


class Stepper:
    __step_code = [[1,0,0,1],
                 [1,0,0,0],
                 [1,1,0,0],
                 [0,1,0,0],
                 [0,1,1,0],
                 [0,0,1,0],
                 [0,0,1,1],
                 [0,0,0,1]]
    def __init__(self, in1: int, in2: int, in3: int, in4: int, steps_per_revolution: int = 4096, step_sleep: int = 0.002):
        self.__pins = (in1, in2, in3, in4)
        self.__spr = steps_per_revolution   # steps per revolution
        self.__ss = step_sleep  # step sleep time in seconds
        self.__msc = 0  # motor step counter
        # Setting GPIO
        GPIO.setmode(GPIO.BCM)
        for pin in self.__pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)
            
    def __del__(self):
        for pin in self.__pins:
            GPIO.output(pin, GPIO.LOW)
    def pause(self):
        for pin in self.__pins:
            GPIO.output(pin, GPIO.LOW)
            
    def step(self, direction: bool = True):
        if direction:
            if self.__msc == 7:
                self.__msc = 0
            else:
                self.__msc += 1
        elif not self.__msc:
            self.__msc = 7
        else:
            self.__msc -= 1
        for pin in range(0, len(self.__pins)):
            GPIO.output(self.__pins[pin], Stepper.__step_code[self.__msc][pin])
        time.sleep(self.__ss)

    # rotate in specified direction
    def rotate(self, steps: int, direction: bool = True):
        for _ in range(steps):
            self.step(direction)
        self.pause()
    # move clockwise in a complete revolution
    def move_cw(self):
        self.rotate(self.__spr)
    # move counter-clockwise in a complete revolution
    def move_ccw(self):
        self.rotate(self.__spr, False)
