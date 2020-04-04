# picoENDEC
Software ENDEC for UNIX. picoENDEC is a small, lightweight, software ENDEC for the OpenENDEC project.

#### Setup
picoENDEC is designed to run on the same system as the OpenENDEC controller and creates a virtual serial port for communication. As such, no additional hardware is needed to run picoENDEC. However, if you have hardware that can take a "News Feed" as an input, picoENDEC can output to a physical serial port to communicate with your ENDEC. Set `PHYSICAL_SERIAL` to the path of your serial port, and `PHYSICAL_BAUD` to that physical serial port's baud rate.

#### Data Sources
By default, picoENDEC decodes CAP data from the NOAA servers. Therefore only weather-related alerts. If you have access to IPAWS, you may configure the `CAP_URI` to your preferred CAP server.

Run `picoendec.py` to start up the software. The serial port will display on screen.

#### License
GNU GPLv3
