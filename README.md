# 🌊 AcquaProber – Collegamenti Hardware

## 🔌 Collegamenti sensori → modulo ADC (ADS1115)

| Sensore              | Pin uscita | Canale ADS1115 |
|----------------------|------------|----------------|
| Sensore **pH**       | AOUT       | A0             |
| Sensore **Torbidità**| AOUT       | A1             |
| Sensore **Conduttività** | AOUT   | A2             |
| Sensore **Temperatura analogico** (LM35 / TMP36) | AOUT | A3 |

> ⚠️ Se usi un sensore di temperatura digitale come il **DS18B20 (quello che usiamo noi)**, vedi sotto: va collegato direttamente al Raspberry Pi.

---

## 🌡 Collegamento sensore temperatura DS18B20 - quello usato da noi (digitale, collegamento 1-Wire)

il sensore di temperatura **DS18B20 ha un collegamento diretto al raspebbry PI non passando per il modulo ADS1115**.

| Pin DS18B20 | Collegamento Raspberry Pi |
|-------------|---------------------------|
| GND         | GND (es. Pin 6)           |
| VCC         | 3.3V (Pin 1)              |
| DATA        | GPIO4 (Pin 7)             |

> ⚠️ È **obbligatoria** una resistenza da **4.7kΩ** tra i pin **DATA** e **VCC**.

---

## 🔁 Collegamenti comuni

- **GND** → unito al GND del Raspberry Pi e al GND dell'ADS1115
- **VCC** → 3.3V o 5V (verifica tensione supportata dai sensori)

---

## 🤖 Collegamenti Raspberry Pi → modulo ADS1115

| Raspberry Pi Pin     | Collega a ADS1115 |
|----------------------|-------------------|
| GPIO2 (Pin 3 – SDA)  | SDA               |
| GPIO3 (Pin 5 – SCL)  | SCL               |
| GND (Pin 6)          | GND               |
| 3.3V / 5V (Pin 1 o 2)| VDD               |

---

## ⚙️ Abilitare interfacce su Raspberry Pi

### ✅ Abilitare I2C
```bash
sudo raspi-config
# Interfacing Options → I2C → Abilita
sudo reboot
```
### ✅ Abilitare 1-Wire (Per DS18B20)
```bash
sudo raspi-config
# Interfacing Options → 1-Wire → Abilita
sudo reboot
```

---
### INSTALLARE LE LIBRERIE UTILI PER IL FUNZIONAMENTO SU RASPBERRY
Per Installare determinate librerie che servono per il funzionamento del software direttamente sul raspberry PI, non si può effettuare l'installazione direttamente nel virtual environment (venv), ma bisogna installare le corrispettive librerie di sistema. Le librerie da installare per questo scopo sono:

- **PyQt5**
- **RPi.GPIO**

Per esempio con RPi.GPIO:
Quando lavori in un ambiente virtuale (venv) su Raspberry Pi, la libreria RPi.GPIO non è installabile direttamente tramite pip, perché è un modulo nativo C fornito tramite i pacchetti di sistema di Raspberry Pi OS.

Il restante delle librerie/moduli possono essere installati tramite il venv (vedi requirments.txt).
Per effettuare tale operazioni sul rasbperry PI bisogna eseguire da terminale i seguenti comandi:
```bash
sudo apt install python3-rpi.gpio # per il modulo RPi.GPIO
sudo apt install python3-pyqt5 python3-pyqt5.qtquick # per PyQt5
```

Dopodichè raggiungere la directory relativa al progetto e creare il venv nel seguente modo:
```bash
python3 -m venv .venv --system-site-packages
source .venv/bin/activate
pip install -r requirments.txt # ti installerà le librerie presenti nel file requirments.txt
```

In questo modo include anche le librerie di sistema utili per il funzionamento del sofwtare.

> ⚠️ Almenochè tu non sia su un dispositivo di tipo ARM come **Raspberry PI**, non appensa esegui il software (python3 main.py) uscirà tale errore:
```bash
Traceback (most recent call last):
  File "/home/fede_chiodi/Desktop/embedded_system/smd_acquaProber/main.py", line 15, in <module>
    from sensors.feeder_servo import open_valve, close_valve, is_valve_open, cleanup
  File "/home/fede_chiodi/Desktop/embedded_system/smd_acquaProber/sensors/feeder_servo.py", line 1, in <module>
    import RPi.GPIO as GPIO
  File "/home/fede_chiodi/Desktop/embedded_system/smd_acquaProber/.venv/lib/python3.13/site-packages/RPi/GPIO/__init__.py", line 23, in <module>
    from RPi._GPIO import *
RuntimeError: This module can only be run on a Raspberry Pi!
```
