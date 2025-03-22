# NAVIGATION
*Below are descriptions of the contents of each file on this repository*

### Source Code
- 'Light App.py' *(contains main program with analytics and forecast module)*

- 'LDT Code.py' *(code for Live Dimming Technology)*

- 'Dummy Duty Cycle Generator.py' *(random mark to space ratio generator to test live graphs)*

- 'sensor_data.csv' *(file that stores and updates mark to space ratio values for live graphs)*

### Software & Hardware List
- 'Components List.xlsx' *(spreadsheet contains more readable version of materials used for project)*

### Instructions
- 'Figure 1.png' – 'Figure 8.png' *(figures mentioned for instructions question on the submission form)*

- 'Instructions (with embedded figures).docx' *(document contains more readable version of instructions)*

### Research
- 'Forecast Model Specification.docx' *(contains cited research into the program’s constants and formulas for calculations)*

- 'LDT Input Circuit Diagram.docx' *(contains in depth explanation of circuit design)*

- 'LDT Output Circuit Diagram.docx' *(contains in depth explanation of circuit design)*


# PROJECT SUMMARY

The Light-Emitting Diode is one of the greatest inventions of the 20th century. Since the early 2000s, LED light bulbs have been praised for their lifespan and energy-saving capabilities—they use at least 75% less energy and last up to 25 times longer than incandescent bulbs.

Despite this, LEDs have still only been adopted by 18% of all UK households. We attribute this poor adoption to society’s lack of information and understanding around lighting. This ignorance has consequences: unnecessary energy waste and astronomically high lighting bills.

Another issue regarding lighting is humans themselves. Even if LEDs were implemented nationwide, we would still have a relatively high electricity consumption due to excess lighting and keeping the lights on when they aren’t needed.

Our project has been dedicated to finding a solution to these issues—approaching it in two ways. We have developed a program that aims to promote energy savings by making consumers more conscious of their energy use. We have also innovated a new mechanism called LDT (Live Dimming Technology) that we estimate can make LEDs around 30% more efficient.

Below, we speak briefly about both solutions.

### Live Dimming Technology

We tackled the issue of excess lighting by automatically adjusting light according to ambient conditions. In the past, this typically involved using a sensor that measured external brightness and fed a PWM controller that adjusted the LED output. A limitation of this technology is that to avoid positive feedback, designers usually must physically shield the sensor from the LED. This reduces the uses of this technology – many spaces do not have naturally unlit areas.

LDT differs from current-day technology by having the LED temporarily turned off whenever readings are taken. We fully prevent a positive feedback loop – without shielding sensors or having energy-intensive filtering algorithms.

We have demonstrated this technology in the footprint of a lamp and are working toward fitting it into a standard light bulb.

### The Program

Our program has been developed to work alongside our live dimming technology. It directly tackles the lack of information around lighting by providing interactive tools to make consumers more conscious of their lighting use. It also provides estimates of energy/cost savings and CO2e prevention if lighting systems used our technology.

The Program consists of two modules. The first module, “Analytics”, provides real-time data on several statistics of a lighting system, such as total power consumption, energy consumption, CO2e emissions, and electricity saved. Currently, it is only based on a single LED, and we are currently working on using it with systems of LEDs. This tool would be beneficial for commercial use, giving shopping malls and offices better insight into their energy use.

The second module, “Forecast”, is a prediction model that we have developed for households to demonstrate the tremendous energy savings achieved when switching from halogens, incandescent, and CFL light bulbs to LEDs. It also shows the further energy savings achieved if all the light bulbs used LDT.

# VIDEOS
## 5 Minute Presentation
[![Presentation video](https://img.youtube.com/vi/xpUQCLLk9Fk/0.jpg)](https://youtu.be/xpUQCLLk9Fk)

## Demonstration
[![Demonstration video](https://img.youtube.com/vi/OyPKLj0iM8w/0.jpg)](https://youtu.be/OyPKLj0iM8w)

