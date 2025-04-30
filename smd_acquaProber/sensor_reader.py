import time
import json
import matplotlib.pyplot as plt
from datetime import datetime
from sensors.ph_sensor import read_ph
from sensors.turbidity_sensor import read_turbidity
from sensors.temperature_sensor import read_temperature
from sensors.conductivity_sensor import read_conductivity

DATA_FILE = 'data_log.json'

# Modalità interattiva
plt.ion()

# Inizializzazione del grafico
fig, ax = plt.subplots(figsize=(12, 8))
lines = {
    'pH': ax.plot([], [], label='pH')[0],
    'turbidity': ax.plot([], [], label='Torbidità')[0],
    'temperature': ax.plot([], [], label='Temperatura (°C)')[0],
    'conductivity': ax.plot([], [], label='Conducibilità')[0],
}

timestamps = []
ph_values = []
turbidity_values = []
temperature_values = []
conductivity_values = []

def read_all_sensors():
    return {
        'ph': round(read_ph(), 2),
        'turbidity': round(read_turbidity(), 2),
        'temperature': round(read_temperature(), 2),
        'conductivity': round(read_conductivity(), 2),
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    }

def save_data(data):
    try:
        with open(DATA_FILE, 'r') as f:
            data_log = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data_log = []

    data_log.append(data)

    with open(DATA_FILE, 'w') as f:
        json.dump(data_log, f, indent=2)

def update_plot():
    # Aggiorna i dati dei plot
    lines['pH'].set_data(timestamps, ph_values)
    lines['turbidity'].set_data(timestamps, turbidity_values)
    lines['temperature'].set_data(timestamps, temperature_values)
    lines['conductivity'].set_data(timestamps, conductivity_values)

    # Ridisegna limiti e layout
    ax.relim()
    ax.autoscale_view()
    ax.set_xlabel('Timestamp')
    ax.set_ylabel('Valori')
    ax.set_title('Andamento dei valori dei sensori nel tempo')
    ax.legend()
    ax.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.draw()
    plt.pause(0.1)

def main_loop(interval=10):
    while True:
        data = read_all_sensors()
        save_data(data)

        # Aggiorna liste
        timestamps.append(datetime.strptime(data['timestamp'], '%Y-%m-%d %H:%M:%S'))
        ph_values.append(data['ph'])
        turbidity_values.append(data['turbidity'])
        temperature_values.append(data['temperature'])
        conductivity_values.append(data['conductivity'])

        print("Dati aggiornati:", data)
        update_plot()
        time.sleep(interval)

if __name__ == '__main__':
    main_loop()