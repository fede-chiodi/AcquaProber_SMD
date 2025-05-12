import platform

def is_raspberry_pi():
    return platform.machine().startswith('arm') or 'raspberrypi' in platform.uname()