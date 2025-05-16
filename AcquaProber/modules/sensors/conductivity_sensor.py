import platform
import board
import busio
from modules.sensors.temperature_sensor import read_temperature
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
chan = AnalogIn(ads, ADS.P2)

VREF = 3.3

def read_conductivity():
    compensation_coeff = 1.0 + 0.02 * (read_temperature() - 25)
    compensation_voltage = chan.voltage / compensation_coeff
    tds_value = (133.42 * (compensation_voltage ** 3) - 255.86 * (compensation_voltage ** 2) + 857.39 * compensation_voltage) * 0.5
    return tds_value
