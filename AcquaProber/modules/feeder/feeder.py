import json
import time
import datetime
import threading
import RPi.GPIO as GPIO
from gpiozero import Servo, Device
from gpiozero.pins.pigpio import PiGPIOFactory
### gpiozero

DEG_90 = 6.5
DEG_0 = 2.5

#jkDevice.pin_factory = PiGPIOFactory(host="127.0.0.1") ## changing pin factory

class Feeder:
    def __init__(self, servo_pin: int, feeder_time: int = -1, opening_time: int = -1):
        ## 100 seconds it's the minimum time, 2 seconds max opening time 
        self.__feeder_time = feeder_time
        self.__opening_time = opening_time
        self.__datas = {}
        self.__filename = "data/settings.json"
        # 0 for inactive, 1 for active
        self.__status = 1
        ## load file datas if invalid values
        if(feeder_time < 100 or opening_time < 0.1 or opening_time > 1):
            self.__load_data()
        # setting servo and initializing to starting position
        GPIO.setmode(GPIO.BCM) 
        GPIO.setup(servo_pin ,GPIO.OUT) 
        self.__servo = GPIO.PWM(servo_pin, 50)  

    ## load settings from json
    def __load_data(self):
        with open(self.__filename, "r") as file:
            self.__datas = json.load(file)
            print(self.__datas)
            self.__feeder_time = self.__datas["feeder_time"] ### feeder time is in seconds
            self.__opening_time = self.__datas["opening_time"]
            
    def __set_data(self, prop: str, value):
        new_json = {}
        with open(self.__filename, "r") as file:
            new_json = json.load(file)
        new_json[prop] = value
        with open(self.__filename, "w") as outfile:
            json.dump(new_json, outfile)
            
        
            
    
    ## stop feeder auto mode
    def stop(self):
        self.__status = 0
    
    ## feed function
    def feed(self):
        self.__servo.start(0)
        self.__servo.ChangeDutyCycle(DEG_90)
        time.sleep(self.__opening_time)
        self.__servo.ChangeDutyCycle(DEG_0)
        self.__servo.stop(0)
        ## food level is refactored after expiration, dummy behaviour
        self.__set_data("food_level", (self.__datas["food_level"] - 1) if self.__datas["food_level"] else 20)
        self.__set_data("last_feed", datetime.datetime.now().strftime("%H:%M"))
        next_date = datetime.datetime.fromtimestamp(int(datetime.datetime.now().timestamp()) + self.__feeder_time)
        self.__set_data("next_feed", next_date.strftime("%H:%M"))
        print(f"{next_date}") 
        
    # opens feeder every __feeder_time seconds
    def run(self):
        self.__status = 1
        start_time = time.time()
        while self.__status:
            if(time.time() - start_time >= self.__feeder_time):
                ## update datas the next time
                self.__load_data()
                self.feed()
                start_time = time.time()
                
                
                
                
def feeder_worker(ipc_dict):
    feeder = Feeder(6) ## fifth from low-left
    t1 = threading.Thread(target=feeder.run())
    t1.start()
    while ipc_dict["status"]:
        continue
    feeder.stop()
    t1.join()
    print("Feeder process terminated correctly!!")



    


