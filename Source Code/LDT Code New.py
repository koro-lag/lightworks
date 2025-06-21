#Imports for using GPIO and using MCP_3008
import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

#Imports for csv  
from datetime import datetime 
import csv
import time 
import pandas as pd

#Initialising the GPIO port we use
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT) 

led = GPIO.PWM(21, 500) #Output channel set to GPIO 21 and PWM freuquency set to 500 Hz
led.start(0) #LED starts as OFF 

#Initialising the ADC 
SPI_PORT = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

modeSetting = pd.read_csv("") #Enter file name!
mode = modeSetting.iloc[0,-1] #Reading last value of first column?

csvFileName = "sensor_data.csv" #CSV file is named sensor_data
fieldNames = ["time", "duty_cycle"] #Row headings are 'time' and 'duty_cycle' respectively

def avgADC(samples = 5): #Samples = 5 means we take 5 readings when this function is called
    readings = [] #We store the readings in the array
    
    led.ChangeDutyCycle(0) #The LED is set to OFF to prevent positive feedback loop
    time.sleep(0.005)

    #During the iteration we append the real time readings to the array
    for _ in range(samples):
        readings.append(mcp.read_adc(0))
        time.sleep(0.001) 
        
    return sum(readings)/len(readings) #We return a calculated average

def pwmAmbience(avgADC):
    #Subject to change depening on location
    if 0 < avgADC < 200:
        return 60
    elif 201 < avgADC < 400:
        return 40
    else: 
        return 0

def pwmFocus(avgADC):
    #Subject to change depening on location
    if 0 < avgADC < 200:
        return 100
    elif 201 < avgADC < 400:
        return 70
    else: 
        return 50
    
def manualMode():
    modeSetting = pd.read_csv("") #Enter file name!
    dc = modeSetting.iloc[1,-1]
    return dc


with open(csvFileName, 'a', newline="") as file:
    csv_writer = csv.DictWriter(file, fieldnames=fieldNames)

    try:
        while True:
            if mode == "ambience":
                avgADCValue = avgADC()
                dc = pwmAmbience(avgADCValue)
                led.ChangeDutyCycle(dc) #Changing LED PWM according to ambiance 
                time.sleep(0.0000001)
            elif mode == "focus":
                avgADCValue = avgADC()
                dc = pwmFocus(avgADCValue)
                led.ChangeDutyCycle(dc) #Changing LED PWM according to ambiance 
                time.sleep(0.0000001)
            else: 
                manualMode()
                led.ChangeDutyCycle(dc) #Changing LED PWM according to ambiance 
                time.sleep(0.0000001)

            currTime = datetime.now().strftime("%H:%M:%S") #When updating the file we include the current time
            
            info = {
                "time": currTime,
                "duty_cycle": (dc/100)
            }
            csv_writer.writerow(info) #Updating the file for communication with our application
            
            print(currTime, dc/100) #Ouput the time and PWM into terminal for testing
            
            file.flush() #Clear buffer for the file
            time.sleep(5) #We only update the file every 5 seconds


    #Stop the program and turn of the LED
    except KeyboardInterrupt:
        led.stop()
        GPIO.cleanup() 




