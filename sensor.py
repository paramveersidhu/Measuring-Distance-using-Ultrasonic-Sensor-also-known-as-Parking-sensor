#!/usr/bin/python3

from signal import signal, SIGTERM, SIGHUP, pause
from time import sleep
from threading import Thread
from gpiozero import DistanceSensor, Buzzer, LED

reading = True
sensor = DistanceSensor(echo=20, trigger=21)
buzzer = Buzzer(24)
led1 = LED(13)
led2 = LED(6)
led3 = LED(26)


def safe_exit(signum, frame):
    exit(1)


signal(SIGTERM, safe_exit)
signal(SIGHUP, safe_exit)


def read_distance():
    while reading:
        distance = sensor.value * 100
        distance = round(distance, 2)
        print("Distance:", distance, "cm")
        sleep(0.1)
        if distance > 20:
            led1.on()
            led2.off()
            led3.off()
        elif 20 > distance > 5:
            led2.on()
            led1.off()
            led3.off()
        else:
            led3.on()
            led2.off()
            led1.off()


try:
    reader = Thread(target=read_distance, daemon=True)
    reader.start()

    pause()

except KeyboardInterrupt:
    pass
finally:
    buzzer.close()
    sensor.close()
    reading = False
