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
