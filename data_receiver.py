import serial
import time
import matplotlib.pyplot as plt
import csv
import os

arduino_port = '/dev/cu.usbmodem11301'  # Replace with your Arduino's port
ser = serial.Serial(arduino_port, 9600)

file_path = '/Users/daniel/Documents/Schule/Physik_Z/arduino_data/'
state_string = "stop"
time_increment = 1 / 1000
time_duration = 10
file_name = None  # Initialize file_name as None

# Create empty lists to store data for plotting
time_values = []
data_values = []

# Function to update the plot
def update_plot():
    plt.clf()  # Clear the previous plot
    plt.plot(time_values, data_values)
    plt.xlabel('Time (s)')
    plt.ylabel('Data')
    plt.title('Real-time Data Plot')
    plt.pause(time_increment/1000000000)  # Pause for a short time to update the plot

while True:
    user_input = input("Press 's' to start data collection\nPress t for a new time duration\nPress 'c' to change the file name\nPress 'q' to end the program  " + '\n')
    
    if user_input == 's':
        if file_name is None:
            print("Please set a file name using 'c' command first.")
        else:
            # Open the CSV file for writing
            os.mkdir(file_path + file_name)
            csv_file_path = file_path + file_name + "_data.csv"
            start_time = time.time()
            counter = 0
            with open(csv_file_path, 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(["Time (s)", "Data"])  # Write header row

                # Clear previous data
                time_values.clear()
                data_values.clear()
                while True:
                    data = ser.readline().decode('utf-8').strip()
                    csv_writer.writerow([time.time()- start_time, data])
                    # Append time and data values for plotting
                    time_values.append(time.time()- start_time)
                    data_values.append(float(data))  # Assuming data is a float
                    update_plot()
                    counter = counter + 1
                    time.sleep(time_increment)
                    #looks whether time has passed
                    if time.time() - start_time >= time_duration:
                        break
                
                print("Data collection finished")
                print("loop has run for: " + str(time.time() - start_time) + " seconds\n")
                print("loop has run " + str(counter) + " times\n")
                file_name = None
                
    elif user_input == 'c':
        file_name = input("Enter a file name: ")
    elif user_input == 't':
        time_duration = int(input("Enter a new time duration(in s): "))
    elif user_input == 'q':
        break

ser.close()
