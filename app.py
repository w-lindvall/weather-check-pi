import datetime
from time import sleep

import dht11
from picamera import PiCamera
import RPi.GPIO as GPIO

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

camera = PiCamera()
check = dht11.DHT11(pin=17)
# set output pin number to match setup

while True:
    result = check.read()
    if result.is_valid():
        camera.start_preview()
        sleep(5)
        # wait 5 seconds to allow for camera to correct exposure
        camera.annotate_text = (datetime.datetime.now().strftime('%d-%m-%y %H:%M')
                                + '\n'
                                + '=' * 20
                                + '\n'
                                + '-{} C'.format(result.temperature)
                                + '\n'
                                + '-{}%'.format(result.humidity))
        camera.capture(('/home/pi/Desktop/{}.jpg'
                        .format('weather_check-' +
                                datetime.datetime.now().strftime(
                                    '%d_%m_%y-%H_%M'))))
        camera.stop_preview()
        sleep(255)
        # wait about 5 minutes until next loop
