import serial
import time
import matplotlib.pyplot as plt
import csv
import os

arduino_port = '/dev/cu.usbmodem11301'  # Replace with your Arduino's port

file_path = '/Users/daniel/Documents/Schule/Physik_Z/arduino_data/'
time_increment = 1 / 1000000000000
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
    plt.pause(time_increment/1000000000000000000000000)  # Pause for a short time to update the plot
    
#saves a plot in a directory
def save_plot(time_values, data_values, file_name):
    plt.figure()
    plt.plot(time_values, data_values)
    plt.xlabel('Time (s)')
    plt.ylabel('Data')
    plt.title('Data Plot')
    plot_file_path = os.path.join(file_path, file_name, file_name + '_plot.png')
    plt.savefig(plot_file_path)
    plt.close()


while True:
    #gives information about the plot
    print("\nPress 's' to start data collection")
    print("Press 't' for a new time duration")
    print("Press 'c' to change the file name")
    print("Press 'q' to end the program")
    user_input = input("Input: ")
    
    #checks whether it should start saving data
    if user_input == 's':
        #checks whether a file name is given
        if file_name is None:
            file_name = input("Set a file name: ")
        else:
            try: 
                #creates a new directory
                os.mkdir(file_path + file_name)
                #open serial
                ser = serial.Serial(arduino_port, 9600)

                #creates a new csv file for wrting
                csv_file_path = file_path + file_name + "/" + file_name + "data.csv"
                #saves the starting time
                start_time = time.time()
                #resets the counter
                counter = 0
                #opens the csv file
                with open(csv_file_path, 'w', newline='') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerow(["Time (s)", "Data"])  # Write header row

                    # Clear previous data
                    time_values.clear()
                    data_values.clear()
                    while True:
                        #reads the data
                        data = ser.readline().decode('utf-8').strip()
                        #writes the data to the csv file
                        csv_writer.writerow([time.time()- start_time, data])
                        # Append time and data values for plotting
                        time_values.append(time.time()- start_time)
                        data_values.append(float(data))  # Assuming data is a float
                        #updates the plot
                        update_plot()
                        #counts the number of cycles
                        counter = counter + 1
                        #looks whether time has passed
                        if time.time() - start_time >= time_duration:
                            break
                    
                    #gives basic information
                    print("Data collection finished\n")
                    print("loop has run for: " + str(time.time() - start_time) + " seconds")
                    print("loop has run " + str(counter) + " times")
                    
                    #saves a plot of the data
                    save_plot(time_values, data_values, file_name)

                    #closes the serial
                    ser.close()
                    #prevents the data from being overwritten
                    file_name = None
            except FileExistsError:
                print("File name already exists")
                file_name = None
    #configure the file name
    elif user_input == 'c':
        file_name = input("Enter a file name: ")
    #configure the time duration
    elif user_input == 't':
        time_duration = int(input("Enter a new time duration(in s): "))
    #exit the code
    elif user_input == 'q':
        break

