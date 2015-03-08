#!/usr/bin/env python

from datetime import datetime
import RPi.GPIO as GPIO
import mpd 
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)	#pin 17 as our 'main' pin

# this will run in another thread when our event is detected  
def main_callback(channel):
    print str(datetime.now())
    client = mpd.MPDClient()
    client.connect("localhost", 6600)
    #print client.status()
    if client.status()['state'] in ('play', 'pause'):
        client.pause()
    else:
        client.play()

# The GPIO.add_event_detect() line below set things up so that  
# when a rising edge is detected on port 23, regardless of whatever   
# else is happening in the program, the function "main__callback" will be run  
GPIO.add_event_detect(17, GPIO.FALLING, callback=main_callback, bouncetime=300)

try:
	while True:
		time.sleep(0.5)
except KeyboardInterrupt:  
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit  
GPIO.cleanup()           # clean up GPIO on normal exit  
