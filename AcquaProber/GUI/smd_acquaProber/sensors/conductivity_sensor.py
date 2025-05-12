import platform

def is_raspberry_pi():
    return platform.machine().startswith('arm') or 'raspberrypi' in platform.uname()

if is_raspberry_pi():
    import board
    import busio
    import adafruit_ads1x15.ads1115 as ADS
    from adafruit_ads1x15.analog_in import AnalogIn

    i2c = busio.I2C(board.SCL, board.SDA)
    ads = ADS.ADS1115(i2c)
    chan = AnalogIn(ads, ADS.P2)

    def read_conductivity():
        voltage = chan.voltage
        conductivity = voltage * 1000  # esempio base
        return conductivity
else:
    import random
    def read_conductivity():
        return random.uniform(100, 500)