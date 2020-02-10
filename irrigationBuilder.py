import RPi.GPIO as GPIO  # input output pins

import time, sys

import spidev  # lets us communicate with SPI (MCP3008)
from multiprocessing import Process  # to run all process at once
from flask import Flask, jsonify, request, make_response, session, g

app = Flask(__name__)
app.secret_key = "super secret"

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)  # Broadcom SOC channel setup
GPIO.setup(20, GPIO.OUT)  # voltage output to avoid soil moisture corrosion

# Variables
delay = 10  # time between updates
ldrChannel = 0  # LDR channel on spi
smsChannel = 5
tempChannel = 2
soilChannel = 7

# SPI object initialize
spi = spidev.SpiDev()  # creates spi object
spi.open(0, 0)  # open spi port 0, device 0 (look into this further
spi.max_speed_hz = 1000000


# takes measurtement for Light Dependent Resistor
# def
def signalProcess(adcnum):
    # read SPI data from the MCP3008, 8 channels in total
    r = spi.xfer2([1, 8 + adcnum << 4, 0])
    data = ((r[1] & 3) << 8) + r[2]
    return data

def SoilProcess(adcnum):
    GPIO.output(18, GPIO.HIGH)
    signal = signalProcess(adcnum)
    GPIO.output(18, GPIO.LOW)


# takes Ultrasoinc Range Finder measurement for depth in reservoir
def urf():
    TRIG = 24
    ECHO = 23

    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)

    GPIO.output(TRIG, False)
    time.sleep(2)
    try:
        while True:
            GPIO.output(TRIG, True)
            time.sleep(1)
            GPIO.output(TRIG, False)

            while GPIO.input(ECHO) == 0:
                pulse_start = time.time()

            while GPIO.input(ECHO) == 1:
                pulse_end = time.time()

            pulse_duration = pulse_end - pulse_start

            distance = pulse_duration * 17150

            distance = round(distance, 1)

            return distance

    except KeyboardInterrupt:
        GPIO.cleanup()


def initiate():
    while True:
        ldr_value = signalProcess()
        time.sleep(delay)





if __name__ == '__main__':
    try:
        while True:
            ldr_value = signalProcess(ldrChannel)
            print("ldr Value %s", ldr_value)
            time.sleep(delay)


    except KeyboardInterrupt:
        print("IOT Irrigation System offline. Goodbye")
        GPIO.cleanup()
        sys.exit()
