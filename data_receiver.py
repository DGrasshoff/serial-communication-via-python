import serial
import time
import matplotlib.pyplot as plt
import csv
import os
import tkinter as tk
from tkinter import Label

# Global variables for the GUI and data collection
arduino_port = '/dev/cu.usbmodem11301'  # Replace with your Arduino's port
file_path = '/Users/daniel/Documents/Schule/Physik_Z/arduino_data/'
time_increment = 1 / 1000000000000
time_duration = 10
file_name = None  # Initialize file_name as None
sensor_value = 0  # Variable to store sensor value

# Create empty lists to store data for plotting
time_values = []
data_values = []

def close_window():
    root.destroy()
# Function to update the plot
def update_plot():
    plt.clf()  # Clear the previous plot
    plt.plot(time_values, data_values)
    plt.xlabel('Time (s)')
    plt.ylabel('Data')
    plt.title('Real-time Data Plot')
    plt.pause(time_increment / 1000000000000000000000000)  # Pause for a short time to update the plot

# Saves a plot in a directory
def save_plot(time_values, data_values, file_name):
    plt.figure()
    plt.plot(time_values, data_values)
    plt.xlabel('Time (s)')
    plt.ylabel('Data')
    plt.title('Data Plot')
    plot_file_path = os.path.join(file_path, file_name, file_name + '_plot.png')
    plt.savefig(plot_file_path)
    plt.close()

# Function to update the sensor value in the GUI
def update_sensor_label(data):
    sensor_label.config(text=f'Sensor Value: {data}')
    
# Function to start data collection
def start_data_collection():
    global file_name
    if file_name is None:
        file_name = file_name_entry.get()
    else:
        try:
            os.mkdir(file_path + file_name)
            ser = serial.Serial(arduino_port, 9600)
            csv_file_path = file_path + file_name + "/" + file_name + "data.csv"
            start_time = time.time()
            counter = 0
            if time_entry.get() is None:
                time_duration = 10
            else:
                time_duration = int(time_entry.get())
            with open(csv_file_path, 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(["Time (s)", "Data"])  # Write header row
                time_values.clear()
                data_values.clear()
                while True:
                    data = ser.readline().decode('utf-8').strip()
                    csv_writer.writerow([time.time() - start_time, data])
                    time_values.append(time.time() - start_time)
                    data_values.append(float(data))
                    update_plot()
                    counter += 1
                    if time.time() - start_time >= time_duration:
                        update_sensor_label(0)
                        break
                    else:
                        update_sensor_label(data)
                print("Data collection finished\n")
                print("Loop has run for: " + str(time.time() - start_time) + " seconds")
                print("Loop has run " + str(counter) + " times")
                save_plot(time_values, data_values, file_name)
                ser.close()
                file_name = None
        except FileExistsError:
            print("File name already exists")
            file_name = None

# Create the GUI window
root = tk.Tk()
root.title("Sensor Data GUI")

# Create a label to display the sensor value
sensor_label = Label(root, text=f'Sensor Value: {sensor_value}')
sensor_label.pack()

# Create an entry widget for entering the file name
file_name_label = Label(root, text="Enter a file name:")
file_name_label.pack()
file_name_entry = tk.Entry(root)
file_name_entry.pack()


time_label = Label(root, text="Enter a measuring time:" )
time_label.pack()
time_entry = tk.Entry(root)
time_entry.pack()

# Create a button to start data collection
start_button = tk.Button(root, text="Start Data Collection", command=start_data_collection)
start_button.pack()

# Create a button to close the window
close_button = tk.Button(root, text="Close", command= close_window)
close_button.pack()

# Start the GUI main loop
root.mainloop()
