#!/usr/bin/env python

from datetime import datetime
import RPi.GPIO as GPIO
import mpd 
import time
from rotary_class import RotaryEncoder

VOLUME_UP = 15 		# GPIO pin 10
VOLUME_DOWN = 14 	# GPIO pin 8
MUTE_SWITCH = 4 	# GPIO pin 7

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)	#pin 17 as our 'main' pin

Last_Vol = 50;	#default volume and var to hold what it was before muting

# this will run in another thread when our main event is detected  
def main_callback(channel):
    print str(datetime.now())
    client = mpd.MPDClient()
    client.connect("localhost", 6600)
    #print client.status()
    if client.status()['state'] in ('play', 'pause'):
        client.pause()
    else:
        client.play()

#Call back routine for the volume control knob
def volume_event(event):
	global Last_Vol	
	client = mpd.MPDClient()
    	client.connect("localhost", 6600)

	if event == RotaryEncoder.CLOCKWISE:
		print "Vol Up"
	elif event == RotaryEncoder.ANTICLOCKWISE:
		print "Vol Down"
	elif event == RotaryEncoder.BUTTONDOWN:
		if client.status()['volume'] == '0':
			client.setvol(Last_Vol)	
		else:
			Last_Vol = int(client.status()['volume'])
			client.setvol(0)
	return

# The GPIO.add_event_detect() line below set things up so that  
# when a rising edge is detected on port 23, regardless of whatever   
# else is happening in the program, the function "main__callback" will be run  
GPIO.add_event_detect(17, GPIO.FALLING, callback=main_callback, bouncetime=300)
volumeknob = RotaryEncoder(VOLUME_UP,VOLUME_DOWN,MUTE_SWITCH,volume_event)

try:
	while True:
		time.sleep(0.2)
except KeyboardInterrupt:  
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit  
GPIO.cleanup()           # clean up GPIO on normal exit  
