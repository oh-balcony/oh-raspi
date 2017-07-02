# Raspberry Pi Balcony Irrigation Controller

Python code for my Raspberry Pi to control the watering of plants on my balcony.

This is part of the [Oh, Balcony!](http://oh-balcony.github.io/) project.

The software allows the control of one or multiple pumps (to pump water from a water tank), valves (to control the flow of water through a system of water hoses), soil moisture sensors (for measuring whether plants should be watered), water level sensors (for measuring the water level in a water tank) and temperature sensors.

## Prerequisites

If you haven't installed an Operating System on your Raspberry Pi then follow my instructions here: [Raspberry Pi Installation](https://github.com/oh-balcony/oh-balcony.github.io/wiki/Raspberry-Pi-Installation)

The following additional software packages will be required:

Python 3:

    sudo apt install python3
    
Python [requests HTTP library](http://docs.python-requests.org):

    sudo apt install python3-requests

Python [gpiozero library](http://gpiozero.readthedocs.io):

    sudo apt install python3-gpiozero

Python [w1thermsensor library](https://github.com/timofurrer/w1thermsensor):

    sudo apt install python3-w1thermsensor

Python spidev library, which is needed for hardware accelerated SPI. It will also work without, but reading Soil Moisture sensors through an MCP3008 Analog-Digital Converter (ADC) will be a little slower (I measured 1.4ms instead of 0.04ms per reading):

    sudo apt install python3-spidev

Additionally the SPI kernel module will need to be enabled. Start the Raspberry Pi configuration tool with

    sudo raspi-config

and select `Interfacing Options` and then `SPI`.

If a 1-wire temperature sensor (DS18S20, DS1822, DS18B20, DS28EA00, DS1825/MAX31850K) is used, then enable also the 1-wire interface. For that add the following line to the file `/boot/config.txt`:

    dtoverlay=w1-gpio,gpiopin=4,pullup=on
    
Note: the `pullup=on` is required if you connected the sensor with a parasitic circuit (GND and VDD connected) as described by [Martin Kompf](https://www.kompf.de/weather/pionewiremini.html). With a non-parasitic circuit it is not needed, as described by [Adafruit](https://cdn-learn.adafruit.com/downloads/pdf/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing.pdf).

Afterwards the Pi will need to be rebooted for the configuration changes to take effect.

## Usage

Clone the git repository:

    git clone https://github.com/oh-balcony/oh-raspi.git

### Configuration

Copy the file `config.sample.py` to `config.py` and adapt it to your needs.

### Starting

Run:

    ./main.py

### Autostart

To automatically start the script when the Raspberry Pi is rebooted, execute:

    crontab -e

... and then add the following line to the crontab:

    @reboot sleep 5 && /home/pi/scripts/oh-raspi/start.sh

(Replace the full path to the script with the location where you installed it.)

### Logrotate

To avoid that the log file grows infinite create the following logrotate rule as `/etc/logrotate.d/oh-raspi`:

```
/home/pi/scripts/oh-raspi/oh-raspi.log {
   weekly
   rotate 4
   compress
   missingok
   copytruncate
}
```
(Replace the path of the logfile with the location where you installed it.)
