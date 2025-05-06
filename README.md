# AcquaProber

COLLEGAMENTI SENSORI ---> MODULO ADC
 
sensore pH → ADS1115 
AOUT → A0
 
sensore Torbidità→ ADS1115
AOUT → A1 
 
sensore Conduttività → ADS1115
AOUT → A2
 
sensore temperatura → ADS1115 (per sensore di temperatura analogico (TMP36 o LM35)
AOUT → A3
 
 
COLLEGAMENTO SENSORE DI TEMPERATURA (DS18B20 - il nostro) 
il sensore di temperatura DS18B20 ha un collegamento diretto al raspebbry PI non passando per il modulo ADS1115.
 
ha 3 pin:
GND
VCC
DATA -> GPIO4 (Pin 7) raspberry PI
⚠️ La resistenza di 4.7kΩ è obbligatoria tra il pin DATA e VCC.
 
COLLEGAMENTI COMUNI
GND → unito al GND di Raspberry Pi e GND dell'ADS1115
VCC → unito a 3.3V o 5V
COLLEGAMENTI RASPBERRY PI ---> MODULO ADC
 
SDA (GPIO2 / Pin 3) -> ADS1115 SDA
SCL (GPIO3 / Pin 5) -> ADS1115 SCL
GND (Pin 6) -> ADS1115  GND + sensori GND
3.3 / 5 V (Pin 1 o 2) -> ADS1115  VDD + sensori VCC
 
 
ABILITARE I2C SU RASPBERRY PI 
sudo raspi-config
Interfacing Options -> I2C -> Abilita
 
sudo reboot
 
ABILITARE 1-WIRE SU RASPBERRY PI (PER SENSORE TEMPERATURA)
sudo raspi-config
Interfacing Options → 1-Wire → Abilita
 
sudo reboot
