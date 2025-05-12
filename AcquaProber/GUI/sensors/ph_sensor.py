# #i2c è una tipologia di comunicazione seriale, viene inizializzato
# i2c = busio.I2C(board.SCL, board.SDA)
# #board.SCL --> GPIO 3 - pin fisico 5
# #board.SDA --> GPIO 2 - pin fisico 3

# #ADS1115 è un convertitore analogico-digitale (ADC), usato in quanto raspberry pi può ricevere solo dati digitali e non analogici.
# #Si crea l'oggeto ADC sul canale i2c

# #creazione di un canale analogico single-ended

# #funzione che serve per la conversione della tensione letta dal sensore pH in un valore pH reale
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
    chan = AnalogIn(ads, ADS.P0)

    def read_ph():
        voltage = chan.voltage
        ph = 7 + ((voltage - 2.5) / 0.18)
        return ph
else:
    import random
    def read_ph():
        return 7 + random.uniform(-0.5, 0.5)