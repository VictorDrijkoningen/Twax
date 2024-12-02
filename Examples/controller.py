#import evdev
from evdev import InputDevice, categorize

#creates object 'gamepad' to store the data
#you can call it whatever you like
gamepad = InputDevice('/dev/input/event11')
gamepadIMU = InputDevice('/dev/input/event12')

#prints out device info at start
print(gamepad)

#evdev takes care of polling the controller in a loop
for event in gamepad.read_loop():
    print(categorize(event))
    print(event)
    print(gamepadIMU.capabilities(True))
    # print(gamepadIMU.upload_effect(1))