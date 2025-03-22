# Import Libraries
import random
import time
from datetime import datetime
import csv

# Constants
MIN_DUTY = 0
MAX_DUTY = 1 # Max Power of LED
DUTY_CYCLE_VARIATION = 0.25

# Initialise Variables
duty_cycle = 0.5

# Headings
field_names = ["time", "duty_cycle"]

with open('sensor_data.csv', 'w', newline='') as file:
    csv_writer = csv.DictWriter(file, fieldnames=field_names)
    csv_writer.writeheader()

with open('sensor_data.csv', 'a', newline='') as file:
        csv_writer = csv.DictWriter(file, fieldnames=field_names)

        while True:
            current_time = datetime.now().strftime("%H:%M:%S")

            duty_cycle += random.uniform(-DUTY_CYCLE_VARIATION, DUTY_CYCLE_VARIATION)

            # Ensure duty cycle stays within bounds
            duty_cycle = max(MIN_DUTY, min(duty_cycle, MAX_DUTY))

            # Data Row
            info = {
                "time": current_time,
                "duty_cycle": round(duty_cycle, 4)
            }

            csv_writer.writerow(info)

            print(current_time, round(duty_cycle, 4))

            file.flush()
            time.sleep(2)
