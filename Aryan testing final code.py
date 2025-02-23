import time 
import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import csv
from datetime import datetime 

csvFileName = "sensor_data.csv"
fieldNames = ["time", "duty_cycle"]

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)

led = GPIO.PWM(21, 500)
led.start(0)

SPI_PORT = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

def avgADC(samples = 5):
    readings = []
    
    led.ChangeDutyCycle(0)
    time.sleep(0.005)
    
    for _ in range(samples):
        readings.append(mcp.read_adc(0))
        time.sleep(0.001) 
        
    return sum(readings)/len(readings)

def pwmFromADC(avgADC):
    if 0 < avgADC < 420:
        return 100
    elif 421 < avgADC < 740:
        return 50
    else:
        return 0

with open(csvFileName, 'a', newline="") as file:
    csv_writer = csv.DictWriter(file, fieldnames=fieldNames)
    try:
        while True:
            avgADCValue = avgADC()
            dc = pwmFromADC(avgADCValue)
            led.ChangeDutyCycle(dc)
            time.sleep(0.0000000000001)
            
            currTime = datetime.now().strftime("%H:%M:%S")
            
            info = {
                "time": currTime,
                "duty_cycle": dc
            }
            csv_writer.writerow(info)
            
            print(currTime, dc)
            
            file.flush()
            time.sleep(5)
    except KeyboardInterrupt:
        led.stop()
        GPIO.cleanup()

