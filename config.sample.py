# Configuration File

# This is the sample configuration file, that I (Hermann) am using for my setup.
# Copy it to 'config.py' and adapt it to your needs.

from components import *

# MCP3008 ADC chip - use a different import if you are using a different chip
# (see http://gpiozero.readthedocs.io/en/stable/api_spi.html#analog-to-digital-converters-adc )
from gpiozero import MCP3008

# needed for 1-wire temperature sensor
from w1thermsensor import W1ThermSensor

controller_name = "controller1"

# Moisture Sensors connected via Analog-Digital-Converter (ADC) chips.
# See class MoistureSensor in components.py for all possible parameters.
# If you have no Moisture Sensors connected, then assign this to an empty dictionary:
# moisture_sensors = {}

moisture_sensors = {
    # 2 resistors setup as voltage dividers. Useful for testing the MCP3008 ADC. Connected to channel 0
    "widerstand": MoistureSensor(MCP3008(channel=0)),

    # DFRobot Capacitive Soil Moisture Sensors, connected via MCP3008 ADC channel 1-3, 1.0 when dry
    "moisture1": MoistureSensor(MCP3008(channel=1), inverse=True),
    "moisture2": MoistureSensor(MCP3008(channel=2), inverse=True),
    "moisture3": MoistureSensor(MCP3008(channel=3), inverse=True),

    # Moisture sensors YL-69 (China), connected via MCP3008 ADC channel 6, 1.0 when dry
    #"moisture6": MoistureSensor(MCP3008(channel=6), inverse=True),

    # Seeed Studio SEN92355P moisture sensor, connected via MCP3008 ADC channel 7, 0.0 when dry
    #"moisture7": MoistureSensor(MCP3008(channel=7))
}

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

# Pumps
# See class Pump in components.py for all possible parameters.
pumps = {
    "pump1": Pump(18)
}

# Valves controlling the flow of water
# See class Valve in components.py for all possible parameters.
valves = {
    "valve1": Valve(5),
    "valve2": Valve(6),
    "valve3": Valve(13),
    "valve4": Valve(19)
}

# Tanks with installed float switches for measuring the water level
# See class WaterLevel and FloatSwitch in components.py for all possible parameters.
water_levels = {
    "tank1": WaterLevel([
        FloatSwitch(pin=21, height=0),
        FloatSwitch(pin=20, height=50),
        FloatSwitch(pin=16, height=100)
    ])
}

# Temperature sensors
temperature_sensors = {
    # Just select the first found 1-Wire temperature sensor
    # To select sensors explicitly see https://github.com/timofurrer/w1thermsensor
    # If no temperature sensor is connected, then just comment out the next line
    "temperature1": W1ThermSensor()
}

# Web Service endpoint
service_base_url = "http://gerty:8080/api/"

# time interval for sending moisture measurements to the server (seconds)
send_measurements_interval = 20  # seconds

# number of measurements that should be aggregated before sending them to the server
aggregated_measurements_count = 6  # default: 6 per minute, i.e. measuring every 10 seconds
