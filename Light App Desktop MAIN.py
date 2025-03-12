'''Imports'''
# For App
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from customtkinter import CTkImage
from PIL import Image
import os

# For Live Graphs
import pandas as pd
import matplotlib.pyplot as plt

# Importing Images / Icons
# def load_image(name):  
#     return ctk.CTkImage(Image.open(os.path.join('Images', name)), size=(40, 40))
# 
# focus_img = load_image('focus.png')
# ambient_img = load_image('ambient.png')
# manual_img = load_image('manual.png')

'''Initialise Variables & Constants'''

DAYS_IN_YEARS = 365.25
HOURS_PER_DAY = 3.9
COST_PER_KWH = 27.03 # Current cost of electricty p/kWh
CO2_PER_KWH = 0.207074 # CO2 equivalent kg/kWh

INCANDESCENT_POWER = 60
HALOGEN_POWER = 45
CFL_POWER = 15
LED_POWER = 8

MAX_VOLTAGE = 12 # Volts
CURRENT = 0.2 # Current going to LDT light circuit
INTERVAL = 5

C_INCANDSCENT_COUNT = 2
C_HALOGEN_COUNT = 3
C_CFL_COUNT = 3
C_LED_COUNT = 26
C_PEOPLE_COUNT= 2
C_ROOM_COUNT =  5 # Living room, kitchen, 2 bedrooms, bathroom

# For Analytics
energy_with_ldl = float(0)
energy_without_ldl = float(0)
energy_savings = float(0)
co2_emissions = float(0)
time_passed = float(0)

# For Forecast
# incandescent_count = int(0)
# halogen_count = int(0)
# cfl_count = int(0)
# led_count = int(0)
# room_count = int(0)
# people_count = int(0)

# Forecast Model ---------------------------------------------------------------------------------------------

def forecast_model(*args):

    try:
        num_room = int(room_count.get())
    except ValueError:
        num_room = 1
    try:
        num_people = int(people_count.get())
    except ValueError:
        num_people = 1
    try:
        num_incandescent = int(incandescent_count.get())
    except ValueError:
        num_incandescent = 0
    try:
        num_halogen = int(halogen_count.get())
    except ValueError:
        num_halogen = 0
    try:
        num_cfl = int(cfl_count.get())
    except ValueError:
        num_cfl = 0
    try:
        num_led = int(led_count.get())
    except ValueError:
        num_led = 0

    # print("Updated Lightbulb Counts:")
    # print(f"Rooms: {num_room}, People: {num_people}, Incandescent: {num_incandescent}, Halogen: {num_halogen}, CFL: {num_cfl}, LED: {num_led}")

    total_watts = (num_incandescent)*(INCANDESCENT_POWER) + (num_halogen)*(HALOGEN_POWER) + (num_cfl)*(CFL_POWER) + (num_led)*(LED_POWER)
    annual_energy = (total_watts/1000)*(HOURS_PER_DAY)*(DAYS_IN_YEARS)*(num_people/num_room)
    annual_cost = (annual_energy)*(COST_PER_KWH)
    annual_co2 = (annual_energy)*(CO2_PER_KWH)

    current_electricty_usage.configure(text = f"Electricty Usage = {annual_energy:.3g} kWh")
    current_light_bill.configure(text = f"CO2 Emissions = {annual_cost:.2f} kg")
    current_co2_emissions.configure(text = f"Electricty Bill = £{annual_co2:.2f}")

    ldt_electricty_usage.configure(text = f"Electricty Usage = {(annual_energy*0.7):.3g} kWh")
    ldt_light_bill.configure(text = f"CO2 Emissions = {(annual_cost*0.7):.2f} kg")
    ldt_co2_emissions.configure(text = f"Electricty Bill = £{(annual_co2*0.7):.2f}")

def reset_to_census():

    room_count.set(f"{C_ROOM_COUNT}")
    people_count.set(f"{C_PEOPLE_COUNT}")
    incandescent_count.set(f"{C_INCANDSCENT_COUNT}")
    halogen_count.set(f"{C_HALOGEN_COUNT}")
    cfl_count.set(f"{C_CFL_COUNT}")
    led_count.set(f"{C_LED_COUNT}")

    forecast_model()

# Analytics Graphs & Stats -----------------------------------------------------------------------------------

''' Power Consumption over Time'''

power_consumption_graph, ax_1 = plt.subplots()
plt.style.use('seaborn-v0_8')

def update_power_consumption_graph():
    data = pd.read_csv('sensor_data.csv')
    
    time = data['time']
    power = MAX_VOLTAGE * CURRENT * data['duty_cycle'] # P = I * V * Duty Cycle (to get average V)
    
    ax_1.clear()
    ax_1.set_xlabel('Time')
    ax_1.set_ylabel('Power Consumption (W)')
    ax_1.plot(time, power)

    # Dynamically adjust the x-axis to avoid too many data points
    if len(time) > 6:  
        step = max(1, len(time) // 6)
        ax_1.set_xticks(range(0, len(time), step))
        ax_1.set_xticklabels(time[::step])
    else:
        ax_1.set_xticks(range(len(time)))
        ax_1.set_xticklabels(time)
    
    power_consumption_canvas.draw()
    
    window.after(INTERVAL * 1000, update_power_consumption_graph)

''' Energy Used over Time '''

energy_consumption_graph, ax_2 = plt.subplots()
plt.style.use('seaborn-v0_8')

def update_energy_consumption_graph():
    global energy_with_ldl
    global energy_without_ldl
    
    data = pd.read_csv('sensor_data.csv')

    energy_with_ldl += (MAX_VOLTAGE * CURRENT * data.iloc[-1]['duty_cycle']) * (INTERVAL / 3600) # E = I * V * t * Duty Cycle (to get average V)
    energy_without_ldl += (MAX_VOLTAGE * CURRENT) * (INTERVAL / 3600) # E = I * V * t 

    ax_2.clear()
    ax_2.bar(['With LDL', 'Without LDL'], [energy_with_ldl, energy_without_ldl])
    ax_2.set_ylabel('Watt-Hour (Wh)')

    # Set the initial y-axis to 10 (for visual appeal)
    initial_y_max = 3
    
    # Dynamically adjust the y-axis if the data exceeds the initial range
    max_value = max(energy_with_ldl, energy_without_ldl)
    if max_value > initial_y_max:
        ax_2.set_ylim(bottom=0, top=max_value + 5) 
    else:
        ax_2.set_ylim(bottom=0, top=initial_y_max) 

    energy_consumption_canvas.draw()

    window.after(INTERVAL * 1000, update_energy_consumption_graph)

''' Estimated Cost Savings & CO2 Emissions'''

def update_labels():
    global energy_savings
    global co2_emissions

    data = pd.read_csv('sensor_data.csv')

    energy_savings += (MAX_VOLTAGE * CURRENT * COST_PER_KWH/1000) * (1 - data.iloc[-1]['duty_cycle']) * (INTERVAL / 3600)
    co2_emissions += (MAX_VOLTAGE * CURRENT) * data.iloc[-1]['duty_cycle'] * CO2_PER_KWH * (INTERVAL / 3600)
    
    # (energy_without_ldl - energy_with_ldl) * ENERGY_COST

    energy_savings_label.configure(text=f'Estimated energy savings: {energy_savings:.4f} Wh')
    co2_emissions_label.configure(text=f'Estimated CO2 emissions: {co2_emissions:.4f} g')

    window.after(INTERVAL * 1000, update_labels)

# Window -----------------------------------------------------------------------------------------------------
# Create the main window
window = ctk.CTk()
window.title('Light App')
window.geometry('1280x800')
#window.resizable(False, False)

ctk.set_appearance_mode('light')


# Control Panel ----------------------------------------------------------------------------------------------

''' Control Panel '''
# Main Frame for Control Panel
control_frame = ctk.CTkFrame(window)
control_frame.pack(fill = 'both', side = 'left', pady = 20, padx = 20)

# Label to display name of frame
control_label = ctk.CTkLabel(control_frame, text = 'Control', font = ('Helvetica Neue', 36, 'bold'))
control_label.pack(pady = 20)

''' Mode Selection Module '''

# Mode Frame
mode_frame = ctk.CTkFrame(control_frame, fg_color='transparent')
mode_frame.pack(pady = 20)

# Mode Label
mode_label = ctk.CTkLabel(mode_frame, text = 'Modes', font = ('Helvetica Neue', 14, 'bold'))
mode_label.pack(pady = 5)

# Focus Button (increases PWM frequency)
focus_button = ctk.CTkButton(mode_frame, width = 60, height = 60, 
                             #image = focus_img,
                             text = None,
                             fg_color = 'white',
                             hover_color = 'light grey'
                             )
focus_button.pack(padx = 10, side = 'left')

# Ambient Button (decreases PWM frequency)
ambient_button = ctk.CTkButton(mode_frame, width = 60, height = 60, 
                               #image = ambient_img,
                               text = None,
                               fg_color = 'white',
                               hover_color = 'light grey'
                               )
                               
ambient_button.pack(padx = 10, side = 'left')

# Manual Button (turns off auto dimming and enables brightness slider)
manual_button = ctk.CTkButton(mode_frame, width = 60, height = 60, 
                              #image = manual_img,
                              text = None,
                              fg_color = 'white',
                              hover_color = 'light grey'
                              )
                              
manual_button.pack(padx = 10, side = 'left')

# Brightness Frame
brightness_frame = ctk.CTkFrame(control_frame, fg_color='transparent')
brightness_frame.pack(pady = 20)

# Off Label
brightness_off_label = ctk.CTkLabel(brightness_frame, text = 'Off', font = ('Helvetica Neue', 12))
brightness_off_label.pack(side = 'left')

# Brightness Slider
brightness_slider = ctk.CTkSlider(brightness_frame)
brightness_slider.pack(side = 'left', padx = 5)
# On Label
brightness_on_label = ctk.CTkLabel(brightness_frame, text = 'On', font = ('Helvetica Neue', 12))
brightness_on_label.pack(side = 'left')

''' Wake up Module '''
# Wake Up Module
wakeup_frame = ctk.CTkFrame(control_frame, fg_color='transparent')
wakeup_frame.pack(pady = 20)

# Wake Up Label
wakeup_label= ctk.CTkLabel(wakeup_frame, text = 'Wake Up', font = ('Helvetica Neue', 14, 'bold'))
wakeup_label.pack()

# Create dropdown values
hours = [f'{i:02}' for i in range(0, 24)] 
minutes = ['00', '15', '30', '45']  

# Time selection variables
hour_var = ctk.StringVar(value='06')
minute_var = ctk.StringVar(value='30')

# Hour dropdown
hour_menu = ctk.CTkComboBox(wakeup_frame, values=hours, variable=hour_var, state='readonly', width=80)
hour_menu.pack(side='left', padx=5)

# Minute dropdown
minute_menu = ctk.CTkComboBox(wakeup_frame, values=minutes, variable=minute_var, state='readonly', width=80)
minute_menu.pack(side='left', padx=5)

# Confirm Button
confirm_button = ctk.CTkButton(wakeup_frame, text='Set Time')
confirm_button.pack(pady=10)


# Analytics ---------------------------------------------------------------------------------------------

''' Analytics '''
# Main frame for Analytics
analytics_frame = ctk.CTkFrame(window)
analytics_frame.pack(side = 'left', expand = True, fill = 'both', pady = 20, padx = 20)

# Label to display name of frame
analytics_label = ctk.CTkLabel(analytics_frame, text = 'Analytics', font = ('Helvetica Neue', 36, 'bold'))
analytics_label.pack(pady = 20)

# Frame to display all of the live data
interior_analytics_frame = ctk.CTkFrame(analytics_frame, fg_color= 'transparent')
interior_analytics_frame.pack(side = 'left', pady = 20, padx = 20)

interior_analytics_frame.grid_columnconfigure(0, weight = 1)
interior_analytics_frame.grid_columnconfigure(1, weight = 1)

interior_analytics_frame.grid_rowconfigure(0, weight = 1)
interior_analytics_frame.grid_rowconfigure(1, weight = 6)
interior_analytics_frame.grid_rowconfigure(2, weight = 1)
interior_analytics_frame.grid_rowconfigure(3, weight = 15)

''' Graphs '''

# Power Consumption over Time
power_consumption_label = ctk.CTkLabel(interior_analytics_frame, text = 'Power Consumption over Time', font = ('Helvetica Neue', 18, 'bold'))
power_consumption_label.grid(row = 0, column = 0, columnspan = 3, sticky='nsew')

power_frame = ctk.CTkFrame(interior_analytics_frame)
power_frame.grid(row=1, column=0, columnspan = 2, padx=10, pady=10, sticky='nsew')

power_consumption_canvas = FigureCanvasTkAgg(power_consumption_graph, power_frame)
power_consumption_canvas.draw()
power_consumption_canvas.get_tk_widget().pack(fill = "x")

# Energy Consumption over Time
energy_consumption_label = ctk.CTkLabel(interior_analytics_frame, text = 'Energy Consumption Comparison', font = ('Helvetica Neue', 18, 'bold'))
energy_consumption_label.grid(row=2, column=0, sticky='nsew')

energy_frame = ctk.CTkFrame(interior_analytics_frame)
energy_frame.grid(row=3, column=0, padx=10, pady=10)

energy_consumption_canvas = FigureCanvasTkAgg(energy_consumption_graph, energy_frame)
energy_consumption_canvas.draw()
energy_consumption_canvas.get_tk_widget().pack()

''' Statistics '''

# Frame for Live Statistics
stats_label = ctk.CTkLabel(interior_analytics_frame, text = 'Other Statistics', font = ('Helvetica Neue', 18, 'bold'))
stats_label.grid(row=2, column=1, sticky='nsew')

stats_frame = ctk.CTkFrame(interior_analytics_frame, fg_color='transparent')
stats_frame.grid(row=3, column=1, padx=10, pady=10, sticky='nsew')

energy_savings_label = ctk.CTkLabel(stats_frame, text='Estimated energy savings: 0.0 Wh', font = ('Helvetica Neue', 14))
energy_savings_label.pack(pady=5)
co2_emissions_label = ctk.CTkLabel(stats_frame, text='Estimated CO2 emissions: 0.0 g', font = ('Helvetica Neue', 14))
co2_emissions_label.pack(pady=5)

# Forecast ---------------------------------------------------------------------------------------------

''' Forecast '''
# Main frame for Forecast
forecast_frame = ctk.CTkFrame(window)
forecast_frame.pack(side = 'left', fill = "both", expand = True, pady = 20, padx = 20)

# Label to display name of frame
forecast_label = ctk.CTkLabel(forecast_frame, text = 'Forecast', font = ('Helvetica Neue', 36, 'bold'))
forecast_label.pack(pady = 20)

# Current Annual Energy Consumption
current_forecast_frame = ctk.CTkFrame(forecast_frame, fg_color= 'transparent')
current_forecast_frame.pack(fill='both', expand=True)

current_forecast_label = ctk.CTkLabel(current_forecast_frame, text = 'Your estimated annual...', font = ('Helvetica Neue', 18, 'bold'))
current_forecast_label.pack()

current_electricty_usage = ctk.CTkLabel(current_forecast_frame, text = "Electricty Usage = 0 kWh", font = ('Helvetica Neue', 14))
current_electricty_usage.pack()

current_light_bill = ctk.CTkLabel(current_forecast_frame, text = "Electricty Bill = £0.00", font = ('Helvetica Neue', 14))
current_light_bill.pack()

current_co2_emissions = ctk.CTkLabel(current_forecast_frame, text = "CO2 Emissions = 0.0 kg", font = ('Helvetica Neue', 14))
current_co2_emissions.pack()

# Switch to LDT Annual Energy Consumption
ldt_forecast_frame = ctk.CTkFrame(forecast_frame, fg_color= 'transparent')
ldt_forecast_frame.pack(fill='both', expand=True)

ldt_forecast_label = ctk.CTkLabel(ldt_forecast_frame, text = 'But with LDT, your estimated annual...', font = ('Helvetica Neue', 18, 'bold'))
ldt_forecast_label.pack()

ldt_electricty_usage = ctk.CTkLabel(ldt_forecast_frame, text = "Electricty Usage = 0 kWh", font = ('Helvetica Neue', 14))
ldt_electricty_usage.pack()

ldt_light_bill = ctk.CTkLabel(ldt_forecast_frame, text = "Electricty Bill = £0.00", font = ('Helvetica Neue', 14))
ldt_light_bill.pack()

ldt_co2_emissions = ctk.CTkLabel(ldt_forecast_frame, text = "CO2 Emissions = 0.0 kg",font = ('Helvetica Neue', 14))
ldt_co2_emissions.pack()

# Adjust Parameters 
parameters_frame = ctk.CTkFrame(forecast_frame, fg_color= 'transparent')
parameters_frame.pack(fill='both', expand=True)

parameters_frame.grid_columnconfigure(0, weight = 1)
parameters_frame.grid_columnconfigure(1, weight = 1)
parameters_frame.grid_rowconfigure(0, weight = 1)
parameters_frame.grid_rowconfigure(1, weight = 1)
parameters_frame.grid_rowconfigure(2, weight = 1)
parameters_frame.grid_rowconfigure(3, weight = 1)
parameters_frame.grid_rowconfigure(4, weight = 1)
parameters_frame.grid_rowconfigure(5, weight = 1)
parameters_frame.grid_rowconfigure(6, weight = 1)
parameters_frame.grid_rowconfigure(7, weight = 2)


parameters_frame_label = ctk.CTkLabel(parameters_frame, text = 'Adjust Parameters', font = ('Helvetica Neue', 18, 'bold'))
parameters_frame_label.grid(row=0, column=0, columnspan = 2, padx=10, pady=10, sticky='nsew')

# Create dropdown values
lightbulb_count = ['0','2','5','10','15','20','25','30','40','50','75','100']
room_and_people_count = ['1','2','3','4','5','6','7','8','9','10','11','12','13']

room_count_label = ctk.CTkLabel(parameters_frame, text = 'No. Rooms ', font = ('Helvetica Neue', 14))
room_count_label.grid(row=1, column=0)

room_count = ctk.CTkComboBox(parameters_frame, width = 70, values = room_and_people_count, command = forecast_model)
room_count.grid(row=1, column=1, sticky = 'w')

people_count_label = ctk.CTkLabel(parameters_frame, text = 'No. People', font = ('Helvetica Neue', 14))
people_count_label.grid(row=2, column=0)

people_count = ctk.CTkComboBox(parameters_frame, width = 70, values = room_and_people_count, command = forecast_model)
people_count.grid(row=2, column=1, sticky = 'w')

incandescent_count_label = ctk.CTkLabel(parameters_frame, text = 'No. Incandescent Bulbs', font = ('Helvetica Neue', 14))
incandescent_count_label.grid(row=3, column=0)

incandescent_count = ctk.CTkComboBox(parameters_frame, width = 70, values = lightbulb_count, command = forecast_model)
incandescent_count.grid(row=3, column=1, sticky = 'w')

halogen_count_label = ctk.CTkLabel(parameters_frame, text = 'No. Halogen Bulbs', font = ('Helvetica Neue', 14))
halogen_count_label.grid(row=4, column=0)

halogen_count = ctk.CTkComboBox(parameters_frame, width = 70, values = lightbulb_count, command = forecast_model)
halogen_count.grid(row=4, column=1, sticky = 'w')

cfl_count_label = ctk.CTkLabel(parameters_frame, text = 'No.Compact Fluorescent Bulbs', font = ('Helvetica Neue', 14))
cfl_count_label.grid(row=5, column=0)

cfl_count = ctk.CTkComboBox(parameters_frame, width = 70, values = lightbulb_count, command = forecast_model)
cfl_count.grid(row=5, column=1, sticky = 'w')

led_count_label = ctk.CTkLabel(parameters_frame, text = 'No. LED Bulbs', font = ('Helvetica Neue', 14))
led_count_label.grid(row=6, column=0)

led_count = ctk.CTkComboBox(parameters_frame, width = 70, values = lightbulb_count, command = forecast_model)
led_count.grid(row=6, column=1, sticky = 'w')

# Reset to Census Button

c_reset = ctk.CTkButton(parameters_frame, text = "Reset to Census", width = 70, command = reset_to_census)
c_reset.grid(row= 7, column = 0, columnspan = 2)









# Start live updates
update_power_consumption_graph()
update_energy_consumption_graph()
update_labels()

# Prevents window from closing automatically
window.mainloop()