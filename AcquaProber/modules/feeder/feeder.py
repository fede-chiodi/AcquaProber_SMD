import json
from gpiozero import Servo ## for Servo
import time
import threading

### gpiozero

class Feeder:
    def __init__(self, servo_pin: int, feeder_time: int = -1, opening_time: int = -1):
        ## 100 seconds it's the minimum time, 2 seconds max opening time 
        self.__feeder_time = feeder_time
        self.__opening_time = opening_time
        # 0 for inactive, 1 for active
        self.__status = 1
        ## load file datas if invalid values
        if(feeder_time < 100 or opening_time < 0.1 or opening_time > 1):
            self.__load_data()
        # setting servo and initializing to starting position
        self.__servo = Servo(servo_pin)
        self.__servo.min()
    
    ## load settings from json
    def __load_data(self):
        with open("data/settings.json") as file:
            j_file = json.load(file)
            self.__feeder_time = j_file["feeder_time"]
            self.__opening_time = j_file["opening_time"]
    
    ## stop feeder auto mode
    def stop(self):
        self.__status = 0
    
    ## feed function
    def feed(self):
        self.__servo.mid()
        time.sleep(self.__opening_time)
        self.__servo.min()
        
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
    
    
    
    
    
                
                
            
        
            
