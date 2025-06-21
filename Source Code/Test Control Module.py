
# For App
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv

# For Live Graphs
import pandas as pd
import matplotlib.pyplot as plt

with open('control_module.csv', "w", newline='') as file:
    csv_writer = csv.DictWriter(file, fieldnames = ["mode", "dc"])
    csv_writer.writeheader()

def focus_mode():
    with open('control_module.csv', "a", newline='') as file:
        csv_writer = csv.DictWriter(file, fieldnames = ["mode", "dc"])
        info = {
            "mode": "focus",
            "dc": 0
        }
        csv_writer.writerow(info)

def ambience_mode():
    with open('control_module.csv', "a", newline='') as file:
        csv_writer = csv.DictWriter(file, fieldnames = ["mode", "dc"])
        info = {
            "mode": "ambience",
            "dc": 0
        }
        csv_writer.writerow(info)
    
def manual_mode():
    dc = brightness_slider.get()

    with open('control_module.csv', "a", newline='') as file:
        csv_writer = csv.DictWriter(file, fieldnames = ["mode", "dc"])
        info = {
            "mode": "manual",
            "dc": dc
        }
        csv_writer.writerow(info)

# Create the main window
window = ctk.CTk()
window.title('Light App')
window.geometry('1280x800')
#window.resizable(False, False)

ctk.set_appearance_mode('light')

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

# Ambient
mode_label = ctk.CTkLabel(mode_frame, text = 'Modes', font = ('Helvetica Neue', 14, 'bold'))
mode_label.pack(pady = 5)

# Focus Mode (high mark to space ratio thresholds)
focus_button = ctk.CTkButton(mode_frame, width = 60, height = 60, 
                             #image = focus_img,
                             text = None,
                             fg_color = 'white',
                             hover_color = 'light grey',
                             command = focus_mode
                             )
focus_button.pack(padx = 10, side = 'left')

# Ambient Mode (low mark to space ratio thresholds)
ambience_button = ctk.CTkButton(mode_frame, width = 60, height = 60, 
                               #image = ambient_img,
                               text = None,
                               fg_color = 'white',
                               hover_color = 'light grey',
                               command = ambience_mode
                               )
                               
ambience_button.pack(padx = 10, side = 'left')

# Manual Mode (manual space ratio thresholds)
manual_button = ctk.CTkButton(mode_frame, width = 60, height = 60, 
                              #image = manual_img,
                              text = None,
                              fg_color = 'white',
                              hover_color = 'light grey',
                              command = manual_mode
                              )
                              
manual_button.pack(padx = 10, side = 'left')

# Brightness Frame
brightness_frame = ctk.CTkFrame(control_frame, fg_color='transparent')
brightness_frame.pack(pady = 20)

# Off Label
brightness_off_label = ctk.CTkLabel(brightness_frame, text = 'Off', font = ('Helvetica Neue', 12))
brightness_off_label.grid(row=0, column=0, padx=(0,5))

# Brightness Slider
brightness_slider = ctk.CTkSlider(brightness_frame,
                                  from_ = 0,
                                  to = 100,
                                  number_of_steps = 5,
                                  command = manual_mode)
brightness_slider.grid(row=0, column=1)

# On Label
brightness_on_label = ctk.CTkLabel(brightness_frame, text = 'On', font = ('Helvetica Neue', 12))
brightness_on_label.grid(row=0, column=2, padx=(5,0))


# Prevents window from closing automatically
window.mainloop()