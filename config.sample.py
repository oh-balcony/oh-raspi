from devices import *

moisture_sensors = {
    # Moisture sensor v1.4 (Conrad), connected via MCP3008 ADC channel 0, 0.0 when dry
    "moisture1": MoistureSensor(channel=0),

    # Moisture sensor YL-69, connected via MCP3008 ADC channel 1, 1.0 when dry
    "moisture2": MoistureSensor(channel=1, inverse=True)
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

# time interval for sending moisture measurements to the server (seconds)
send_measurements_interval = 1  # seconds

# number of measurements that should be aggregated before sending them to the server
aggregated_measurements_count = 30
