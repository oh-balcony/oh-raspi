#!/usr/bin/env python3

try:
    from config import *
except ImportError as err:
    print("The configuration file config.py does not exist. Have a look at config.sample.py for reference. (" +
          str(err) + ")")
    exit(1)

print()
print("The following moisture sensors are available:")
for name, sensor in moisture_sensors.items():
    print(" * moisture_sensors[\""+name+"\"]")
print("You can enter moisture_sensors[NAME].value to read one those.")

print()
print("The following temperature sensors are available:")
for name, sensor in temperature_sensors.items():
    print(" * temperature_sensors[\""+name+"\"]")
print("You can enter temperature_sensors[NAME].get_temperature() to read one those.")

print()
print("The following water level sensors are available:")
for name, sensor in water_levels.items():
    print(" * water_levels[\""+name+"\"]")
print("You can enter water_levels[NAME].value to read one those. Use water_levels[NAME].float_switch_values to read details about the individual float switches.")

print()
print("The following valves are available:")
for name, sensor in valves.items():
    print(" * valves[\""+name+"\"]")
print("You can enter valves[NAME].open() or .close() to open/close a valve.")

print()
print("The following pumps are available:")
for name, sensor in pumps.items():
    print(" * pumps[\""+name+"\"]")
print("You can enter pumps[NAME].on() or .off() to turn a pump on/off. WARNING: Only turn a pump on, if at least one of the valves is open.")

print()
print("Here is an interactive python shell:")
print("Enter exit() to stop testing.")
