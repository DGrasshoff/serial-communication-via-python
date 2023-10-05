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
    plot_file_path = os.path.join(file_path, file_name, file_name + "_plot.png")
    plt.savefig(plot_file_path)
    plt.close()

# Function to update the sensor value in the GUI
def update_sensor_label(data):
    sensor_label.config(text=f'Sensor Value: {data}')
    
def update_average(input):
    average_label.config(text=f'Average Sensor Value: {input}')
    
# Function to start data collection
def start_data_collection():
    global file_name
    try:
        file_name = str(file_name_entry.get())
        os.mkdir(file_path + file_name)
        csv_file_path = file_path + file_name + "/" + file_name + "data.csv"
        start_data_visualization()
        with open(csv_file_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["Time (s)", "Sensor Value", "Voltage(V)"])  # Write header row

            for x in range(len(data_values)):
                voltage = data_values[x] * 5/1023
                csv_writer.writerow([time_values[x], data_values[x], voltage])

        save_plot(time_values, data_values, file_name)
        file_name = None
    except FileExistsError:
        print("File name already exists")
        
        
def start_data_visualization():
        ser = serial.Serial(arduino_port, 9600)
        start_time = time.time()
        counter = 0
        update_counter =  0
        try:
            time_duration = int(time_entry.get())
        except:
            time_duration = 10
        time_values.clear()
        data_values.clear()
        average_sum = 0
        average_counter = 0
        average = 0
        n = 1
        while True: 
            try:
                data = int(ser.readline().decode('utf-8').strip())
                time_values.append(time.time() - start_time)
                data_values.append(int(data))
                average_sum += data
                average_counter += 1
            except:
                print("Error Serial")
            if time.time() - start_time >= n * 0.5:
                average = average_sum / average_counter
                average_counter = 0
                average_sum = 0
                n += 1
            if update_counter == 10:
                update_plot()
                update_sensor_label(data)
                update_average(average)
                update_counter = 0
            else:
                update_counter += 1
            counter += 1
            if time.time() - start_time >= time_duration:
                end_time = time.time() - start_time
                break
        print("Data collection finished\n")
        print("Loop has run for: " + str(end_time) + " seconds")
        print("Loop has run " + str(counter) + " times")
        ser.close()


# Create the GUI window
root = tk.Tk()
root.title("Sensor Data GUI")

# Create a label to display the sensor value
sensor_label = Label(root, text=f'No input')
sensor_label.pack()

average_label = Label(root, text=f'No Input')
average_label.pack()
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

# Create a button to start data collection
start_2_button = tk.Button(root, text="Show Data", command=start_data_visualization)
start_2_button.pack()

# Create a button to close the window
close_button = tk.Button(root, text="Close", command= close_window)
close_button.pack()

# Start the GUI main loop
root.mainloop()
