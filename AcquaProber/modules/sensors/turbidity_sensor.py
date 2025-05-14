import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
chan = AnalogIn(ads, ADS.P1)

def read_turbidity():
    voltage = chan.voltage
    ntu = -1120.4 * (voltage ** 2) + 5742.3 * voltage - 4352.9
    return ntu
