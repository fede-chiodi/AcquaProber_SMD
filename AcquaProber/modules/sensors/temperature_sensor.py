from w1thermsensor import W1ThermSensor

sensor = W1ThermSensor()

def read_temperature():
    return sensor.get_temperature()
