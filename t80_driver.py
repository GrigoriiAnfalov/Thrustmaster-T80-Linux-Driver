import evdev
import uinput
import sys

# I used to use this, but the device path changes.
# DEVICE_PATH = '/dev/input/event24' 

DEVICE_NAME = "Thrustmaster Thrustmaster T80"  # Change this to match your wheel's exact name

def find_device_by_name(name_query):
    """Scans connected devices and returns the path of the matching device."""
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        if name_query.lower() in device.name.lower():
            return device.path
    return None

# Find the device dynamically
device_path = find_device_by_name(DEVICE_NAME)

if not device_path:
    print(f"Error: Could not find any device containing '{DEVICE_NAME}'")
    print("Available devices:")
    for path in evdev.list_devices():
        try:
            dev = evdev.InputDevice(path)
            print(f"  - {dev.name} (Path: {path})")
        except PermissionError:
            print(f"  - [Permission Denied] (Path: {path})")
    sys.exit(1)

try:
    wheel = evdev.InputDevice(device_path)
    wheel.grab()
    print(f"Successfully grabbed: {wheel.name} on {device_path}")
except Exception as e:
    print(f"Error: Could not open device. Did you forget 'sudo'? \n{e}")
    sys.exit(1)

# DEFINE THE EXACT XBOX 360 LAYOUT FOR ROBLOX
virtual_device_events = [
    # Main Buttons
    uinput.BTN_SOUTH,  # A Button
    uinput.BTN_EAST,   # B Button
    uinput.BTN_NORTH,  # X Button
    uinput.BTN_WEST,   # Y Button
    uinput.BTN_SELECT, # Back
    uinput.BTN_START,  # Start
    
    # Sticks MUST be 16-bit signed (-32768 to 32767) for Roblox/Wine
    uinput.ABS_X + (-32768, 32767, 16, 128),  # Steering
    uinput.ABS_Y + (-32768, 32767, 16, 128),  # Left Stick Y, not used
    
    # Triggers MUST be 0 to 1023 or 0 to 255
    uinput.ABS_Z + (0, 1023, 0, 0),   # Left Trigger (Brake)
    
    uinput.ABS_RX + (-32768, 32767, 16, 128), # Right Stick X (Camera); 
    uinput.ABS_RY + (-32768, 32767, 16, 128), # Right Stick Y (Camera)
    uinput.ABS_RZ + (0, 1023, 0, 0),  # Right Trigger (Gas)
]

# Create device with official Microsoft Xbox 360 IDs (Vendor: 0x045e, Product: 0x028e)
with uinput.Device(
    virtual_device_events, 
    name="Microsoft X-Box 360 pad",
    vendor=0x045E,
    product=0x028E,
    version=0x0110
) as vdev:
    
    print("Virtual Xbox Controller is now live for Roblox!")
	
	# Main event loop
    for event in wheel.read_loop():
    
    	# Axis input
    	# The D-Pad is treated as an axis, and I was too lazy to implement it, but you got this, I believe in you!
        if event.type == evdev.ecodes.EV_ABS:

            # 1. Steering Handling
            if event.code == evdev.ecodes.ABS_X:
                # Maps the T80 0-255 raw steering to the 16-bit signed range Roblox expects
                # Formula: (val / 255) * 65535 - 32768
                normalized_steering = int((event.value / 255.0) * 65535) - 32768
                vdev.emit(uinput.ABS_X, normalized_steering)
            
            # 2. Gas Pedal Handling (T80 0-255 -> Xbox 0-1023)
            elif event.code == evdev.ecodes.ABS_RY:
                normalized_gas = int((event.value / 255.0) * 1023)
                vdev.emit(uinput.ABS_RZ, normalized_gas)
                
            # 3. Brake Pedal Handling (T80 0-255 -> Xbox 0-1023)
            elif event.code == evdev.ecodes.ABS_RX:
                normalized_brake = int((event.value / 255.0) * 1023)
                vdev.emit(uinput.ABS_Z, normalized_brake)
        
        # Buttons
        # Share options and PS buttons are not implemented because I got lazy and did not need them, but you can probably follow the logic from here.
        elif event.type == evdev.ecodes.EV_KEY:

			# Binds left paddle (BTN_WEST) to X (BTN_NORTH)
            if event.code == evdev.ecodes.BTN_WEST:
            	vdev.emit(uinput.BTN_NORTH, event.value)
            
            # Binds right paddle (BTN_Z) to Y (BTN_WEST)
            elif event.code == evdev.ecodes.BTN_Z:
            	vdev.emit(uinput.BTN_WEST, event.value)
            
            # Binds square or "X" (BTN_SOUTH) to X (BTN_NORTH)
            elif event.code == evdev.ecodes.BTN_SOUTH:
            	vdev.emit(uinput.BTN_NORTH, event.value)
            
            # Binds triangle or "Y" (BTN_NORTH) to Y (BTN_WEST)
            elif event.code == evdev.ecodes.BTN_NORTH:
            	vdev.emit(uinput.BTN_WEST, event.value)
            
            # Binds circle or "B" (BTN_SELECT) to B (BTN_EAST)
            elif event.code == evdev.ecodes.BTN_C:
            	vdev.emit(uinput.BTN_EAST, event.value)
                        
            # Binds cross or "A" (BTN_START) to A (BTN_SOUTH)
            elif event.code == evdev.ecodes.BTN_EAST:
            	vdev.emit(uinput.BTN_SOUTH, event.value)
            
            
            # These were set up for Midnight Racing: Tokyo, because I couldn't be bothered to figure out the bumpers. You should delete the lines below if you want a more standard experience.
            
            # Binds L3 or Select (BTN_SELECT) to B (BTN_EAST)
            elif event.code == evdev.ecodes.BTN_SELECT:
            	vdev.emit(uinput.BTN_EAST, event.value)
                        
            # Binds R3 or Start (BTN_START) to A (BTN_SOUTH)
            elif event.code == evdev.ecodes.BTN_START:
            	vdev.emit(uinput.BTN_SOUTH, event.value)
            
            
