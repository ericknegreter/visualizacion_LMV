import Adafruit_DHT
import mysql.connector
import time 
import os 
import subprocess, datetime

# Set sensor tpye: Options are DHT11, DHT22 or AM2301
sensor=Adafruit_DHT.DHT11

#Set GPIO sensor is connected to
gpio=17

while True:
    humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)
    if humidity is not None and temperature is not None:
        print('Temp={0:0.1f}*C Humidity={1:0.1f}%'.format(temperature, humidity))
    else:
        print('Fallo')
