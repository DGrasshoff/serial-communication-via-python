This project measures the analog value of the A0 arduino pin and then sends this value via serial. 
The python code then saves the data in a csv file and further saves a plot of the data over
time. Further the data is plotted in realtime too.
One can configure the measurement duration

data_sender.ino - is the file the arduino is programmed with(sends the data value every Millisecond)
data_receiver.py - is the python file, which saves the data
