# Thrustmaster-T80-Linux-Driver
A basic linux driver for the racing wheel Thrustmaster T80 using python3 with evdev and uinput.

# How to Install:
* Install Python 3
* pip install evdev python-uinput
* Run evtest in console to see all usb devices connected
* Change the name of the wheel on line 8 to whatever your T80 is named

# How to Run:
* sudo python3 t80_driver.py
* sudo is required because the script crosses some high security boundaries that the kernel limits

# How to Modify:
* You can snoop the inputs from the wheel using evtest
* Use the current code as reference, the comments are (hopefully) good enough that you can see the pattern
* Vibe code the rest
