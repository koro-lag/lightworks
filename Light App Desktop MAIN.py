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
#    return ctk.CTkImage(Image.open(os.path.join("Images", name)), size=(40, 40))

# focus_img = load_image("focus.png")
# ambient_img = load_image("ambient.png")
# manual_img = load_image("manual.png")

'''Initialise Variables & Constants'''

ENERGY_COST = 0.02486 # Current cost of electricty p/Wh
CO2 = 0.196 # CO2 equivalent p/Wh
MAX_VOLTAGE = 12 # Volts
CURRENT = 2 # Amps
INTERVAL = 2

energy_with_ldl = 0
energy_without_ldl = 0
energy_savings = 0
co2_emissions = 0
time_passed = 0
# Subprograms ------------------------------------------------------------------------------------------------

# Selecting time for Wakeup Module
def get_time():
    selected_time = f'{hour_var.get()}:{minute_var.get()}'
    print('Selected Time:', selected_time)

# Analytics Graphs & Stats -----------------------------------------------------------------------------------

''' Power Consumption over Time'''

power_consumption_graph, ax_1 = plt.subplots()
plt.style.use('seaborn-v0_8')

def update_power_consumption_graph():
    data = pd.read_csv('sensor_data.csv')
    
    time = data['time']
    power = MAX_VOLTAGE * CURRENT * data['duty_cycle'] # P = I * V * Duty Cycle (to get average V)
    
    ax_1.clear() 
    ax_1.set_title('Power Consumption of LED') 
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
    ax_2.set_title('Energy Consumption Comparison')
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

    energy_savings += (MAX_VOLTAGE * CURRENT * ENERGY_COST) * (1 - data.iloc[-1]['duty_cycle']) * (INTERVAL / 3600)
    co2_emissions += (MAX_VOLTAGE * CURRENT) * data.iloc[-1]['duty_cycle'] * CO2 * (INTERVAL / 3600)
    
    # (energy_without_ldl - energy_with_ldl) * ENERGY_COST

    energy_savings_label.configure(text=f"Estimated energy savings: {energy_savings:.4f} Wh")
    co2_emissions_label.configure(text=f"Estimated CO2 emissions: {co2_emissions:.4f} g")

    window.after(INTERVAL * 1000, update_labels)

# Window -----------------------------------------------------------------------------------------------------
# Create the main window
window = ctk.CTk()
window.title('Light App')
window.geometry('1280x800')
window.resizable(False, False)

ctk.set_appearance_mode('light')


# Control Panel ----------------------------------------------------------------------------------------------

''' Control Panel '''
# Main Frame for Control Panel
control_frame = ctk.CTkFrame(window)
control_frame.pack(side = 'left', fill = 'both', expand = True, pady = 20, padx = 20)

# Label to display name of frame
control_label = ctk.CTkLabel(control_frame, text = 'Control', font = ("Helvetica Neue", 36, "bold"))
control_label.pack(pady = 20)

''' Mode Selection Module '''

# Mode Frame
mode_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
mode_frame.pack(pady = 20)

# Mode Label
mode_label = ctk.CTkLabel(mode_frame, text = 'Modes', font = ("Helvetica Neue", 14, "bold"))
mode_label.pack(pady = 5)

# Focus Button (increases PWM frequency)
focus_button = ctk.CTkButton(mode_frame, width = 60, height = 60, 
                             #image = focus_img,
                             text = None,
                             fg_color = "white",
                             hover_color = "light grey"
                             )
focus_button.pack(padx = 10, side = 'left')

# Ambient Button (decreases PWM frequency)
ambient_button = ctk.CTkButton(mode_frame, width = 60, height = 60, 
                               #image = ambient_img,
                               text = None,
                               fg_color = "white",
                               hover_color = "light grey"
                               )
                               
ambient_button.pack(padx = 10, side = 'left')

# Manual Button (turns off auto dimming and enables brightness slider)
manual_button = ctk.CTkButton(mode_frame, width = 60, height = 60, 
                              #image = manual_img,
                              text = None,
                              fg_color = "white",
                              hover_color = "light grey"
                              )
                              
manual_button.pack(padx = 10, side = 'left')

# Brightness Frame
brightness_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
brightness_frame.pack(pady = 20)

# Off Label
brightness_off_label = ctk.CTkLabel(brightness_frame, text = "Off", font = ("Helvetica Neue", 12))
brightness_off_label.pack(side = "left")

# Brightness Slider
brightness_slider = ctk.CTkSlider(brightness_frame)
brightness_slider.pack(side = 'left', padx = 5)
# On Label
brightness_on_label = ctk.CTkLabel(brightness_frame, text = "On", font = ("Helvetica Neue", 12))
brightness_on_label.pack(side = "left")

''' Wake up Module '''
# Wake Up Module
wakeup_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
wakeup_frame.pack(pady = 20)

# Wake Up Label
wakeup_label= ctk.CTkLabel(wakeup_frame, text = "Wake Up", font = ("Helvetica Neue", 14, "bold"))
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
confirm_button = ctk.CTkButton(wakeup_frame, text='Set Time', command=get_time)
confirm_button.pack(pady=10)


# Analytics ---------------------------------------------------------------------------------------------

''' Analytics '''
# Main frame for Analytics
analytics_frame = ctk.CTkFrame(window)
analytics_frame.pack(side = 'left', fill = 'both', expand = True, pady = 20, padx = 20)

# Label to display name of frame
analytics_label = ctk.CTkLabel(analytics_frame, text = 'Analytics', font = ("Helvetica Neue", 36, "bold"))
analytics_label.pack(pady = 20)

''' Graphs '''
# Frame for Live Graphs
graph_frame = ctk.CTkFrame(analytics_frame, fg_color="transparent")
graph_frame.pack(fill='both', expand=True, pady=10, padx=10)

graph_frame.grid_columnconfigure(0, weight=1)
graph_frame.grid_columnconfigure(1, weight=5)

# Power Consumption over Time
power_frame = ctk.CTkFrame(graph_frame)
power_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

power_consumption_canvas = FigureCanvasTkAgg(power_consumption_graph, power_frame)
power_consumption_canvas.draw()
power_consumption_canvas.get_tk_widget().pack(fill="both", expand=True)

# Energy Consumption over Time
energy_frame = ctk.CTkFrame(graph_frame)
energy_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

energy_consumption_canvas = FigureCanvasTkAgg(energy_consumption_graph, energy_frame)
energy_consumption_canvas.draw()
energy_consumption_canvas.get_tk_widget().pack(fill="both", expand=True)


''' Statistics '''
# Frame for Live Statistics
stats_frame = ctk.CTkFrame(analytics_frame, fg_color="transparent")
stats_frame.pack(fill = 'x', expand = True, pady = 10, padx = 10)

energy_savings_label = ctk.CTkLabel(stats_frame, text="Estimated energy savings: 0.0 Wh")
energy_savings_label.pack(pady=5)
co2_emissions_label = ctk.CTkLabel(stats_frame, text="Estimated CO2 emissions: 0.0 g")
co2_emissions_label.pack(pady=5)

# Start live updates
update_power_consumption_graph()
update_energy_consumption_graph()
update_labels()

# Prevents window from closing automatically
window.mainloop()
