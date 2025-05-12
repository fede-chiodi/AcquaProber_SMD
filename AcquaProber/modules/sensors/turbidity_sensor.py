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
    chan = AnalogIn(ads, ADS.P1)

    def read_turbidity():
        voltage = chan.voltage
        ntu = -1120.4 * (voltage ** 2) + 5742.3 * voltage - 4352.9
        return ntu
else:
    import random
    def read_turbidity():
        return random.uniform(10, 100)