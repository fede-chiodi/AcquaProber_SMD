import platform

def is_raspberry_pi():
    return platform.machine().startswith('arm') or 'raspberrypi' in platform.uname()

if is_raspberry_pi():
    from w1thermsensor import W1ThermSensor
    sensor = W1ThermSensor()

    def read_temperature():
        return sensor.get_temperature()
else:
    import random
    def read_temperature():
        return random.uniform(18.0, 26.0)