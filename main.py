#!/usr/bin/env python3

from time import sleep, clock
from pprint import pprint
from statistics import median

try:
    from config import *
except ImportError as err:
    print("The configuration file config.py does not exist. Have a look at config.sample.py for reference. (" + str(err)
          + ")")
    exit(1)


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

# TODO
# pump = Pump(17)
#
# pump.on()
# sleep(100)

# valve = Valve(17)
# print("Initial")
# sleep(2)
# while True:
#     print("Close")
#     valve.close()
#     sleep(2)
#     print("Open")
#     valve.open()
#     sleep(2)

# float_switch = FloatSwitch(27, active_wet=False)
# while True:
#     print("Wet? " + str(float_switch.is_wet()))
#     sleep(0.5)

# while True:
#     print(water_levels["tank1"].value)
#     sleep(0.2)

main()
