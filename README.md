# Raspberry Pi Balcony Irrigation Controller

Python code for my Raspberry Pi to control the watering of plants on my balcony.

This is part of the [Oh, Balcony!](http://oh-balcony.github.io/) project.

The software allows the control of one or multiple pumps (to pump water from a water tank), valves (to control the flow of water through a system of water hoses), soil moisture sensors (for measuring whether plants should be watered) and water level sensors (for measuring the water level in the tank).

## Prerequisites

If you haven't installed an Operations System on your Raspberry Pi then follow my instructions here: [Raspberry Pi Installation](https://github.com/oh-balcony/oh-balcony.github.io/wiki/Raspberry-Pi-Installation)

The following additional software packages will be required:

Python 3:

    sudo apt-get install python3
    
Python [requests HTTP library](http://docs.python-requests.org):

    sudo apt-get install python3-requests

Python [gpiozero library](http://gpiozero.readthedocs.io):

    sudo apt-get install python3-gpiozero

Python spidev library, which is needed for hardware accelerated SPI. It will also work without, but reading Soil Moisture sensors through an MCP3008 Analog-Digital Converter (ADC) will be a little slower (I measured 1.4ms instead of 0.04ms per reading):

    sudo apt-get install python3-spidev

Additionally the SPI kernel module will need to be enabled. Start the Raspberry Pi configuration tool with

    sudo raspi-config

and select `Advanced Options` and then `SPI`. Afterwards the Pi will need to be rebooted for the changes to take effect.

## Usage

Clone the git repository:

   git clone 

### Configuration

Copy the file `config.sample.py` to `config.py` and adapt it to your needs.

### Starting

Run:

    ./main.py

### Autostart

To automatically start the script when the Raspberry Pi is rebooted, execute:

    crontab -e

... and then add the following line to the crontab:

    @reboot sleep 5 && screen -dmS oh-raspi /home/pi/scripts/oh-raspi/main.py

(Replace the full path to the script with the location where you installed it.)
