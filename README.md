# CAN-Bridges
Python tools for bridging CAN bus to other protocols such as UDP. Intended primarily for use with PlotJuggler. Presently only UDP is supported, WebSocket support may be added in the future.

#Supported CAN Interfaces
Currently PCAN and IXXAT USB-CAN adapters are supported, as well as socketCAN on Linux. The script can be easily modified to include other options supported by python-can. Presently only the PCAN interface on Windows has been tested.

# Dependencies
- Python 3 (developed with 3.6.4)
- python-can
- [cantools]([url](https://cantools.readthedocs.io/en/latest/))
- [gooey]([url](https://github.com/chriskiehl/Gooey))

# Installation
Installation of CAN drivers is not covered here. See the appropriate manufacturer website for your USB-CAN adapter.

## Installation of Dependencies 
```
pip install python-can
pip install cantools
pip install gooey
```
# Usage
Call the script from the command line to launch the GUI:
    ```
    python can_udp_bridge.py
    ```
    
Follow the instrucitons on-screen for configuring the tool:

![image](https://user-images.githubusercontent.com/2954254/183314754-9b70f138-bf70-4fa8-808b-b4114b2bf03d.png)

## Plotjuggler Configuration
To configure PlotJuggler, select the UDP Server streaming option and then click "start" to launch the configuration screen:

![image](https://user-images.githubusercontent.com/2954254/183314910-939b742e-116d-42c9-9639-bbda47d6e6aa.png)


An example configuration for PlotJuggler is shown below:

![image](https://user-images.githubusercontent.com/2954254/183314890-49b04579-9f36-4062-bfc6-18a72edf6b4c.png)

