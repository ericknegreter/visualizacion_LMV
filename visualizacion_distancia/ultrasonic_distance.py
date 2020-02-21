#Libraries
import RPi.GPIO as GPIO
import time
import mysql.connector
import os 
import subprocess, datetime

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#set GPIO Pins
GPIO_TRIGGER = 23
GPIO_ECHO = 24
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(25, GPIO.OUT) #25
#test host
hosts = ('google.com', 'kernel.org', 'yahoo.com')
localhost = ('10.0.5.246')

def ping(host):
    ret = subprocess.call(['ping', '-c', '3', '-W', '5', host],
            stdout=open('/dev/null', 'w'),
            stderr=open('/dev/null', 'w'))
    return ret == 0

def net_is_up():
    print ("[%s] Checking if network is up..." % str(datetime.datetime.now()))
    
    xstatus = 1
    if ping(localhost):
        print ("[%s] Network is up!" % str(datetime.datetime.now()))
        xstatus = 0
        
    if xstatus:
        time.sleep(10)
        print ("[%s] Network is down :(" % str(datetime.datetime.now())) 
        time.sleep(25)

    return xstatus

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance
 
if __name__ == '__main__':
    try:
        estado = 0
        while True:
            dist = distance()
            print("Measured Distance = %.1f cm" % dist)
            if(dist >= 33 and dist <= 38):
                if(estado != 0):
                    while True:
                        if(net_is_up() == 0):
                            #Connection to database LMV and insert on registro table new field with mysql
                            #registro
                            mydb = mysql.connector.connect(host="10.0.5.246", user="LMV_ADMIN", passwd="LABORATORIOT4", database="LMV")
                            mycursor = mydb.cursor()
                            sql = "UPDATE a_visualizacion SET estado = 0 WHERE dispositivo='transfer'"
                            mycursor.execute(sql)
                            mydb.commit()
                            print(mycursor.rowcount, "record affected.")
                            time.sleep(1)
                            #END of mysql
                            estado = 0
                            break
                    #Led End
                    GPIO.output(25, False) #13
            else:
                if(estado != 1):
                    while True:
                        if(net_is_up() == 0):
                            #Connection to database LMV and insert on registro table new field with sql
                            #registro
                            mydb = mysql.connector.connect(host="10.0.5.246", user="LMV_ADMIN", passwd="LABORATORIOT4", database="LMV")
                            mycursor = mydb.cursor()
                            sql = "UPDATE a_visualizacion SET estado = 1 WHERE dispositivo='transfer'"
                            mycursor.execute(sql)
                            mydb.commit()
                            print(mycursor.rowcount, "record affected.")
                            time.sleep(1)
                            #END of mysql
                            estado = 1
                            break
                    #Led Start
                    GPIO.output(25, True) #25
            time.sleep(5)

        # Reset by pressing CTRL + C
        #except KeyboardInterrupt:
        #    print("Measurement stopped by User")
    except ValueError:
        print("Measurement stopped by Error")
    except OSError as err:
        print("OS error: {0}".format(err))
        #except:
        #    print("No controlado")
        #GPIO.cleanup()
