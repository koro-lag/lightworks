import time 
import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import csv
from datetime import datetime 

csvFileName = "sensor_data.csv" # CSV file is named sensor_data
fieldNames = ["time", "duty_cycle"] # Row headings are 'time' and 'duty_cycle' respectively

# Initialising the GPIO port we use
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT) 

led = GPIO.PWM(21, 500) # Output channel set to GPIO 21 and PWM freuquency set to 500 Hz
led.start(0) # LED starts as OFF 

# Initialising the ADC 
SPI_PORT = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

def avgADC(samples = 5): # samples = 5 means we take 5 readings when this function is called
    readings = [] # We store the readings in the array
    
    led.ChangeDutyCycle(0) # The LED is set to OFF to prevent positive feedback loop
    time.sleep(0.005)

    # During the iteration we append the real time readings to the array
    for _ in range(samples):
        readings.append(mcp.read_adc(0))
        time.sleep(0.001) 
        
    return sum(readings)/len(readings) # We return a calculated average

# In this function we use selection to output a suitable PWM for the calculated ambiance, these values can be calibrated with testing
def pwmFromADC(avgADC):
    if 0 < avgADC < 200:
        return 100
    elif 201 < avgADC < 400:
        return 50
    else:
        return 0

with open(csvFileName, 'a', newline="") as file:
    csv_writer = csv.DictWriter(file, fieldnames=fieldNames)
    try:
        while True: # This iteration will run unless Ctrl+C is pressed to interrupt the sequence
            avgADCValue = avgADC() # Storing avgerage ADC value
            dc = pwmFromADC(avgADCValue) # Storing mark-to-space ratio
            led.ChangeDutyCycle(dc) # Changing LED PWM according to ambiance 
            time.sleep(0.0000000000001) 
            
            currTime = datetime.now().strftime("%H:%M:%S") # When updating the file we include the current time
            
            info = {
                "time": currTime,
                "duty_cycle": (dc/100)
            }
            csv_writer.writerow(info) # Updating the file for communication with our application
            
            print(currTime, dc/100) # Ouput the time and PWM into terminal for testing, this code can be removed 
            
            file.flush() # Clear buffer for the file
            time.sleep(5) # We only update the file every 5 seconds

    # Stop the program and turn of the LED
    except KeyboardInterrupt:
        led.stop()
        GPIO.cleanup() 
