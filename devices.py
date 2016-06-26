from gpiozero import DigitalOutputDevice, MCP3008


class Pump(DigitalOutputDevice):
    """
        A water pump controlled by a relay.

        Relays are usually active on low.
    """
    def __init__(self, pin=None, active_high=False, initial_value=False):
        super(Pump, self).__init__(pin, active_high, initial_value)


class MoistureSensor:
    """
        A moisture sensor connected to an Analog-Digital-Converter chip (MCP3008 by default).

        If the moisture sensor is 0 when dry then set inverse to False (default), if it is 1 when dry then set inverse
        to True.
    """
    def __init__(self, channel=0, inverse=False, chip=MCP3008):
        self._sensor = chip(channel=channel)
        self.inverse = inverse

    @property
    def value(self):
        if self.inverse:
            return 1 - self._sensor.value
        else:
            return self._sensor.value
