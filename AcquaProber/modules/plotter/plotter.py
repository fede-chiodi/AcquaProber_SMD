from stepper import Stepper
from threading import Thread

class Plotter:
    __max_steps = 10500  # steps per revolution
    def __init__(self, stp1: Stepper, stp2: Stepper, stp3: Stepper = None):
        self.__stp1 = stp1  # X-axis stepper
        self.__stp2 = stp2  # Y-axis stepper
        self.__stp3 = stp3  # Z-axis stepper (optional)
        self.__step_pos = [0, 0]  # position in steps
        ## resetting to start position
        print("Inizializzazione del plotter in corso, attendere...")
        #self.rst()
        
    # put both x and y steppers to the initial position
    def rst(self):
        self.__stp1.rotate(Plotter.__max_steps, False)
        self.__stp2.rotate(Plotter.__max_steps, False)
        ch = input("Assicurarsi che le rotelle siano inserite nei binari (0, 0), digitare Y: ")
        if ch.upper() != "Y":
            exit(1)
    
    def moveX(self, x: int):
        # mapping the position to actual step value
        if 0 <= x <= 100:
            # mapping to actual step number
            x = int(Plotter.__max_steps * x / 100)
            if x < self.__step_pos[0]:
                self.__stp1.rotate(self.__step_pos[0] - x, False)
                self.__step_pos[0] -= self.__step_pos[0] - x
            else:
                self.__stp1.rotate(x - self.__step_pos[0], True)
                self.__step_pos[0] += x - self.__step_pos[0]
    
    def moveY(self, y: int):
        # mapping the position to actual step value
        if 0 <= y <= 100:
            # mapping to actual step number
            y = int(Plotter.__max_steps * y / 100)
            if y < self.__step_pos[1]:
                self.__stp2.rotate(self.__step_pos[1] - y, False)
                self.__step_pos[1] -= self.__step_pos[1] - y
            else:
                self.__stp2.rotate(y - self.__step_pos[1], True)
                self.__step_pos[1] += y - self.__step_pos[1]
    
    # requires: status: str, mode: str, x_pos: int, y_pos: int from main process     
    def run(self, ipc_dict):
        # controlla in continuo la modalità, si avvicina ad ogni iterazione al valore prefissato
        x_dir = True
        y_dir = True
        while ipc_dict["status"]:
            # quando il valore cambia, riconvertiamo da centesimi a steps
            if(ipc_dict["mode"]):
                if 0 <= ipc_dict["x_pos"] <= 100:
                    x_steps_todo = int(Plotter.__max_steps * ipc_dict["x_pos"] / 100)
                    # if value changed
                    if(x_steps_todo != self.__step_pos[0]):
                        # set correct direction
                        if(x_steps_todo < self.__step_pos[0]):
                            x_dir = False
                        else:
                            x_dir = True
                        # move to new position
                        self.__step_pos[0] += 1 if x_dir else -1
                        self.__stp1.step(x_dir)
                    else:
                        self.__stp1.pause()
                        
                if 0 <= ipc_dict["y_pos"] <= 100:
                    y_steps_todo = int(Plotter.__max_steps * ipc_dict["y_pos"] / 100)
                    if(y_steps_todo != self.__step_pos[1]):
                        if(y_steps_todo < self.__step_pos[1]):
                            y_dir = False
                        else:
                            y_dir = True
                        self.__step_pos[1] += 1 if y_dir else -1
                        self.__stp2.step(y_dir)
                    else:
                        self.__stp2.pause()
            else:
                # otherwise natural movement
                x_dir = False if self.__step_pos[0] == Plotter.__max_steps else (True if self.__step_pos[0] == 0 else x_dir)
                y_dir = False if self.__step_pos[1] == Plotter.__max_steps else (True if self.__step_pos[1] == 0 else y_dir)
                self.__step_pos[0] += 1 if x_dir else -1
                self.__step_pos[1] += 1 if y_dir else -1
                self.__stp1.step(x_dir)
                self.__stp2.step(y_dir)
                print(f"{self.__step_pos[0]} {self.__step_pos[1]} {x_dir} {y_dir}")
                
                
                
                
                
                
            
##### TO IMPORT ######

def plotter_worker(ipc_dict):
    stp_x = Stepper(23, 24, 25, 8)
    stp_y = Stepper(17, 27, 22, 10)
    plotter = Plotter(stp_x, stp_y)
    plotter.run(ipc_dict)

#### calibrazione , conta il massimo numero di step
#stp_x = Stepper(23, 24, 25, 8)
#stp_x.rotate(10000, False)
#input("Assicurarsi che la rotellina sia fuori il binario, spingere poi questo per reinserirla al primo scatto, digitare y quando pronto: ")
#while True:
#    stp_x.step(True)
#    c = input("Controlla che sia inserito, digitare y se ok: ")
#    if c == "y":
#        break
#step_counter = 0
#while True:
#    stp_x.rotate(2000)
#    step_counter += 2000
#    c = input("Continuare se si pensa che manca ancora questa distanza: ")
#    if(c != "y"):
#        break
#print("Aggiusta la precisione")
#while True:
#    stp_x.rotate(10)
#    step_counter += 10
#    c = input("Continuare: ")
#    if(c != 'y'):
#        break


#print(f"Step massimi: {step_counter}")

ipc = {"mode": 1, "x_pos": 20, "y_pos": 40, "status": 1}
ipc["x_pos"] = int(input("Pos x: "))
ipc["y_pos"] = int(input("Pos y: "))
plotter_worker(ipc)



