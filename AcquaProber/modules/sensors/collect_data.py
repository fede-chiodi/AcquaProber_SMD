import time
import json
from modules.sensors.ph_sensor import read_ph
from modules.sensors.turbidity_sensor import read_turbidity
from modules.sensors.temperature_sensor import read_temperature
from modules.sensors.conductivity_sensor import read_conductivity

DATA_FILE = "data/sensors_datas.json"

def read_sensors():
    return {
        "pH": read_ph(),
        "Turbidity": read_turbidity(),
        "Temperature": read_temperature(),
        "TDS": read_conductivity()
     }

def collect_data(shared_dict):
    while shared_dict["status"]:
       sensors_datas = read_sensors()
       shared_dict.update(sensors_datas)
       try:
           with open(DATA_FILE, "r") as file:
               file_log = json.load(file)
       except (FileNotFoundError, json.JSONDecodeError):
           file_log = []

       file_log.append(sensors_datas)

       with open(DATA_FILE, "w") as file:
           json.dump(file_log, file, indent=2)

       time.sleep(2) ## every 2 seconds

