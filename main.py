#!/usr/bin/env python3

from gpiozero import DigitalOutputDevice
from time import sleep


class Pump(DigitalOutputDevice):
    """
        A water pump controlled by a relay.

        Relays are usually active on low.
    """
    def __init__(self, pin=None, active_high=False, initial_value=False):
        super(Pump, self).__init__(pin, active_high, initial_value)


pump = Pump(17)

pump.on()
sleep(100)
