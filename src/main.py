# 01: Import necessary libraries
from PIL import Image, ImageTk
import tkinter as tk
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

# Constants for energy levels and update intervals
BASELINE_ENERGY = 0.5  # Baseline energy level in µW
SPIKE_ENERGY = 1.5     # Energy spike level in µW
UPDATE_INTERVAL = 1000  # Interval in ms for live updates

# 02: Initialize main window
root = tk.Tk()
root.title("Mimosa Energy")
root.geometry("800x600")

# 03: Define paths for open and closed plant images
current_dir = os.path.dirname(os.path.abspath(__file__))
open_image_path = os.path.join(current_dir, "images/open.png")
close_image_path = os.path.join(current_dir, "images/close.png")

# Load, resize, and convert images for display
plant_img_open = ImageTk.PhotoImage(Image.open(open_image_path).resize((200, 200)))
plant_img_closed = ImageTk.PhotoImage(Image.open(close_image_path).resize((200, 200)))

# Display initial plant image in a label
plant_label = tk.Label(root, image=plant_img_open)
plant_label.pack()

# 04: Welcome label at the top
welcome_label = tk.Label(root, text="Welcome to the MIMOSA Energy Dashboard")
welcome_label.pack()

# 10: Function to simulate sensor data
def get_sensor_data():
    # Simulate sensor data for energy production
    return random.uniform(BASELINE_ENERGY, SPIKE_ENERGY)

# 05: Create figure and axis for Matplotlib chart
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Configure plot limits and styling
ax.set_title('Energy Production (µW)', color='blue')
ax.set_xlabel('Time (seconds)', color='green')
ax.set_ylabel('Energy (µW)', color='green')
ax.set_ylim(0, 2)  # Y-axis limit from 0 to 2 µW
ax.grid(True, linestyle='--', linewidth=0.5)

# Initialize plot line and data lists
line, = ax.plot([], [], lw=2, color='red')
time_data = []
energy_data = []

# 06
# Function to update chart with new energy value
def update_chart():
    global time_data, energy_data, current_energy
    time_data.append(len(time_data))  # Append time as length of time_data
    energy_data.append(current_energy)  # Append current energy value

    # Keep only the last 60 seconds of data
    if len(time_data) > 60:
        time_data, energy_data = time_data[-60:], energy_data[-60:]

    # Update line data and redraw chart
    line.set_data(range(len(time_data)), energy_data)
    ax.set_xlim(0, 60)  # Ensure x-axis is fixed
    canvas.draw()


# 07
# Function to simulate continuous energy readings
def live_update():
    global current_energy
    update_chart()  # Update chart with current energy
    if update_active:  # Check if updates are active
        root.after(UPDATE_INTERVAL, live_update)  # Schedule the next update
    else:
        current_energy = BASELINE_ENERGY  # Reset to baseline if stopped


# 08
# Function to simulate energy spike and decay
def simulate_single_plant():
    global current_energy
    plant_label.config(image=plant_img_closed)  # Change to closed plant image
    current_energy = SPIKE_ENERGY  # Immediate spike
    update_chart()  # Update chart with immediate spike

    # Inner function for decaying energy back to baseline
    def decay_to_baseline():
        global current_energy
        if current_energy > 0:
            current_energy -= 0.1  # Smooth decay to 0.0
            update_chart()
            root.after(100, decay_to_baseline)
        else:
            current_energy = BASELINE_ENERGY  # Finally set back to 0.5 µW
            update_chart()
            plant_label.config(image=plant_img_open)  # Revert image to open

    root.after(100, decay_to_baseline)

# Bind click event to plant image for spike simulation
plant_label.bind("<Button-1>", lambda e: simulate_single_plant())


# 09: Initialize energy level
current_energy = BASELINE_ENERGY
update_chart()  # Initial update to set base level

# 11: Function to display flow chart
def display_flow_chart():
    flow_chart = """
    Energy Production Flow Chart:
    1. Plant Movement Detected by Sensors
    2. Energy Spike Generated (1.5 µW)
    3. Energy Decay to Baseline (0.5 µW)
    4. Energy Stored in Battery or Flywheel
    5. Energy Utilization for Dashboard Visualization
    """
    flow_chart_label.config(text=flow_chart)

# Flow chart display button
flow_chart_button = tk.Button(root, text="Show Flow Chart", command=display_flow_chart)
flow_chart_button.pack()

# Flow chart label
flow_chart_label = tk.Label(root, text="")
flow_chart_label.pack()

# 12: Function to simulate flywheel mechanism
def simulate_flywheel():
    global flywheel_energy
    flywheel_energy += current_energy  # Add current energy to flywheel storage
    flywheel_energy_label.config(text=f"Flywheel Energy: {flywheel_energy:.2f} µW")
    root.after(UPDATE_INTERVAL, simulate_flywheel)

# Initialize flywheel energy storage
flywheel_energy = 0.0

# Flywheel energy label
flywheel_energy_label = tk.Label(root, text=f"Flywheel Energy: {flywheel_energy:.2f} µW")
flywheel_energy_label.pack()

# Start flywheel simulation
simulate_flywheel()

# 13: Function to update battery status
def update_battery_status():
    global battery_energy
    if current_energy > BASELINE_ENERGY:
        battery_energy += current_energy - BASELINE_ENERGY  # Charge battery with excess energy
    else:
        battery_energy = max(0, battery_energy - BASELINE_ENERGY + current_energy)  # Discharge battery to maintain baseline

    battery_energy_label.config(text=f"Battery Energy: {battery_energy:.2f} µW")
    root.after(UPDATE_INTERVAL, update_battery_status)

# Initialize battery energy storage
battery_energy = 0.0

# Battery energy label
battery_energy_label = tk.Label(root, text=f"Battery Energy: {battery_energy:.2f} µW")
battery_energy_label.pack()

# Start battery status updates
update_battery_status()

# 14
update_active = False  # Variable to control if updates are active

def start_updates():
    global update_active
    update_active = True  # Activate live updates
    live_update()  # Start live updates

def stop_updates():
    global update_active
    update_active = False  # Deactivate live updates

# Create Start and Stop buttons
start_button = tk.Button(root, text="Start", command=start_updates)
start_button.pack(side=tk.LEFT, padx=20)

stop_button = tk.Button(root, text="Stop", command=stop_updates)
stop_button.pack(side=tk.RIGHT, padx=20)


#last block
# Start main Tkinter loop
root.mainloop()


n