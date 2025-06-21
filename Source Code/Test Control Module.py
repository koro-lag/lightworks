# For App
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv

# For Live Graphs
import pandas as pd
import matplotlib.pyplot as plt

with open('control_module.csv', "w", newline='') as file:
    csv_writer = csv.DictWriter(file, fieldnames=["mode", "dc"])
    csv_writer.writeheader()

current_mode = 'focus'
def control(mode_chosen):
    global current_mode
    current_mode = mode_chosen.lower

    if current_mode in ('focus', 'ambience'):
        with open('control_module.csv', 'a', newline='') as file:
            csv_writer = csv.DictWriter(file, fieldnames=["mode", "dc"])
            csv_writer.writerow({
                'mode': current_mode,
                'dc': 0                   # ← changed key from 'duty_cycle' to 'dc'
            })

def manual_value(slider_value):
    # only do something if we're in Manual mode
    if current_mode == "manual":
        with open('control_module.csv', 'a', newline='') as file:
            csv_writer = csv.DictWriter(file, fieldnames=["mode", "dc"])
            csv_writer.writerow({
                'mode': current_mode,
                'dc': slider_value        # ← changed key from 'duty_cycle' to 'dc'
            })

# Create the main window
window = ctk.CTk()
window.title('Light App')
window.geometry('1280x800')

ctk.set_appearance_mode('light')

''' Control Panel '''
control_frame = ctk.CTkFrame(window)
control_frame.pack(fill='both', side='left', pady=20, padx=20)

control_label = ctk.CTkLabel(control_frame, text='Control', font=('Helvetica Neue', 36, 'bold'))
control_label.pack(pady=20)

''' Mode Selection Module '''
mode_frame = ctk.CTkFrame(control_frame, fg_color='transparent')
mode_frame.pack(pady=20)

mode_label = ctk.CTkLabel(mode_frame, text='Modes', font=('Helvetica Neue', 14, 'bold'))
mode_label.pack(pady=5)

mode_button = ctk.CTkSegmentedButton(
    mode_frame, width=180, height=60,
    values=["Focus", "Ambience", "Manual"],
    command=control
)
mode_button.pack(pady=(20,10))

# Brightness Frame
brightness_frame = ctk.CTkFrame(control_frame, fg_color='transparent')
brightness_frame.pack(pady=20)

brightness_off_label = ctk.CTkLabel(brightness_frame, text='Off', font=('Helvetica Neue', 12))
brightness_off_label.grid(row=0, column=0, padx=(0,5))

brightness_slider = ctk.CTkSlider(
    brightness_frame,
    from_=0, to=100,
    number_of_steps=5,
    command=manual_value
)
brightness_slider.grid(row=0, column=1)

brightness_on_label = ctk.CTkLabel(brightness_frame, text='On', font=('Helvetica Neue', 12))
brightness_on_label.grid(row=0, column=2, padx=(5,0))

window.mainloop()
