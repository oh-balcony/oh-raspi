#!/usr/bin/env python3

from time import sleep, clock
from pprint import pprint
from statistics import median
import json
import requests
import logging

logger = logging.getLogger('oh-balcony')

try:
    from config import *
except ImportError as err:
    print("The configuration file config.py does not exist. Have a look at config.sample.py for reference. (" +
          str(err) + ")")
    exit(1)


def main():
    print("Oh, Balcony!")

    all_off()

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
            store_and_change_state(aggregated_values)
        processing_time = clock() - start_time
        sleep_time = max(measure_interval - processing_time, 0)
        sleep(sleep_time)


def all_off():
    for pump in pumps.values():
        pump.off()

    for valve in valves.values():
        valve.close()


def measure_moisture(moisture_values):
    for name, sensor in moisture_sensors.items():
        value = sensor.value
        moisture_values[name].append(value)


def aggregate_values(values_map):
    return {name: median(values) for name, values in values_map.items()}


def clear_values_map(values_map):
    for values in values_map.values():
        del values[:]


def store_and_change_state(aggregated_values):

    water_level_values = {name: water_level.value for name, water_level in water_levels.items()}
    pump_values = {name: pump.is_active for name, pump in pumps.items()}
    valve_values = {name: valve.is_open for name, valve in valves.items()}

    payload = {"moisture": aggregated_values,
               "tanks": water_level_values,
               "pumps": pump_values,
               "valves": valve_values}

    # debugging output for float switches
    # for name, water_level in water_levels.items():
    #     print(name + ": ")
    #     pprint(water_level.float_switch_values)
    # pprint(water_level_values)

    pprint(payload)

    instructions = send_and_get_instructions(payload)

    pprint(instructions)

    pump_instructions = instructions["pumps"]
    valve_instructions = instructions["valves"]

    for name, pump in pumps.items():
        if name in pump_instructions and pump_instructions[name]:
            pump.on()
        else:
            pump.off()

    for name, valve in valves.items():
        if name in valve_instructions and valve_instructions[name]:
            valve.open()
        else:
            valve.close()

    for name, state in instructions["pumps"].items():
        if name not in pumps:
            logger.error("Ignoring instructions for unknown pump " + name)
    for name, state in instructions["valves"].items():
        if name not in valves:
            logger.error("Ignoring instructions for unknown valve " + name)


def send_and_get_instructions(payload):
    headers = {'content-type': 'application/json'}
    instructions = {"pumps": {}, "valves": {}}  # default: all off/closed
    try:
        response = requests.post(get_service_endpoint("store"), data=json.dumps(payload), headers=headers, timeout=5.0)
        response.raise_for_status()

        instructions = response.json()
    except Exception as e:
        logger.exception("Communication error with server", e)
    return instructions


def get_service_endpoint(endpoint):
    if service_base_url.endswith("/"):
        return service_base_url + endpoint
    else:
        return service_base_url + "/" + endpoint


# TODO
# pumps["pump1"].on()
# sleep(100)

# valve = valves["valve1"]
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
