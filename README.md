# VisualTimer
A basic visual round timmer for the Raspberry pi and the Blinkt led strip

This timmer was created to put an end to the loud and annoying tantrums of children when have to share something based on time, ex. when only one can use the trampolin.

It uses the blinkt led strip for the Raspberry pi to display duration of current session (by a gradient of color) and change period (by flashing).

The timmer is a python object whose properties set the timer settings and methods its actions

## Properties

- timer.brightness:
Led brightness as a float in the range [0,1]
    
- timer.session_duration:
Session duration in minutes as an integer
    
- timer.change_duration:
Time between sessions in seconds as integrer
    
- timer.timer_version:
Colors to create the timmer gradient 
1 - Green/Red version
2 - Blue/Red version
    
- timer.standby_version:
1 - Random Colors
2 - Color Loop

## Methods

- timer.start()
Start the timer

- timer.stop()
Stop the timer

- timer.end()
turn off the led strip
