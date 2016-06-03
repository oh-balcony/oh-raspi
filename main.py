#!/usr/bin/env python3

from gpiozero import DigitalOutputDevice, MCP3008
from time import sleep, clock
from pprint import pprint
from statistics import median


class Pump(DigitalOutputDevice):
    """
        A water pump controlled by a relay.

        Relays are usually active on low.
    """
    def __init__(self, pin=None, active_high=False, initial_value=False):
        super(Pump, self).__init__(pin, active_high, initial_value)

# Empirical values for Moisture sensors:
# Moisture sensor v1.4 (Conrad)
#   Air:                 0
#   Sand/Earth dry:      0.01
#   Skin:                0.06
#   Earth almost dry:    0.07
#   Sand/Earth wet:      0.12
#   Earth wet:           0.42
#   Sand/Earth very wet: 0.45
#   Water:               0.46
#   Wired:               0.73

moisture_sensors = {
    # Moisture sensor v1.4 (Conrad)
    "moisture1": MCP3008(channel=0),

    # TODO connect additional moisture sensors
    # "moisture2": MCP3008(channel=1)
}

# time interval for sending moisture measurements to the server (seconds)
send_measurements_interval = 1  # seconds

# number of measurements that should be aggregated before sending them to the server
aggregated_measurements_count = 30


def measure_moisture(moisture_values):
    for name, sensor in moisture_sensors.items():
        value = sensor.value
        moisture_values[name].append(value)


def aggregate_values(values_map):
    return {name: median(values) for name, values in values_map.items()}


def clear_values_map(values_map):
    for values in values_map.values():
        del values[:]


def store(aggregated_values):
    pprint(aggregated_values)
    # TODO send to server


def main():
    # time between two measurements (seconds)
    measure_interval = send_measurements_interval / aggregated_measurements_count

    print("Measuring every", measure_interval, "seconds, aggregating", aggregated_measurements_count,
          "values and sending them to the server every", send_measurements_interval, "seconds.")

    moisture_values = {moistureSensorName: [] for moistureSensorName in moisture_sensors.keys()}
    moisture_values_count = 0

    while True:
        start_time = clock()
        measure_moisture(moisture_values)
        moisture_values_count += 1
        if moisture_values_count >= aggregated_measurements_count:
            moisture_values_count = 0
            aggregated_values = aggregate_values(moisture_values)
            clear_values_map(moisture_values)
            store(aggregated_values)
        processing_time = clock() - start_time
        sleep_time = max(measure_interval - processing_time, 0)
        sleep(sleep_time)


print("Oh, Balcony!")
main()

# TODO pump
# pump = Pump(17)
#
# pump.on()
# sleep(100)
