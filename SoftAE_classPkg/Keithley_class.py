###CHRIS JOHNSON###
#This python class is storing a lot of the Keithley code so we don't have to worry about
#pasting it into large AE jupyter notebooks. 

##***WIP***##


#Import packages
import pyvisa
import time
import numpy as np
import os
import csv
# rm = pyvisa.ResourceManager()
# print(rm.list_resources())

# Initialize Keithley DAQ6510 Multimeter:
# com_mm.clear()
# com_mm.write("*IDN?\n")
# print(com_mm.read())

# com_mm.clear()
# com_mm.close()
# com_mm = rm.open_resource('USB0::0x05E6::0x6510::04433485::INSTR')

class Keithley:


    def __init__(self, ID, rm):
        self.ID = ID
        global com_mm #This fixed the continuous opening - global. 
        #Make sure not to define com_mm in any other function.
        com_mm = rm.open_resource(ID)
        #global 

    def reset_func_write(self):
        #Attempt writing SCPI function: - write function to reset scripts on multimeter
        script_name = "destroy"
        com_mm.write("loadscript "+ script_name)

        #   Attempt writing TSP functions and controlling Keithley
        #the script below works, but cannot delete scripts from the multimeter...
        com_mm.write("reset()")
        com_mm.write("beeper.beep(1, 600)")
        com_mm.write("script.delete(string.format('W_sweep'))")
        com_mm.write("endscript")   

    def reset_func_read(self):
        com_mm.write("destroy.run()")

    def multi_measure(self, num_measurements):
        """Function takes number of AE measurements, measures set of results.
        1. Initialize DAQ code.
        2. Measure on 8 channels.
        3. Output each channel into CSV"""
        #Section 1, write the DAQ communication code
        ##Note - we should decide if we initialize in here too. I say no and make a startup function.
        self.reset_func_write()
        self.reset_func_read()
        script_name = "W_sweep"
        com_mm.write("loadscript "+ script_name)
        com_mm.write("function W_sweep()")
        #Load initial parameters
        com_mm.write("reset()")
        com_mm.write("scanCount=10")
        com_mm.write("sampleCount=8")
        com_mm.write("defbuffer1.capacity = scanCount * sampleCount")
        #Set up each channel measurement, we want to sweep voltage, measure current
        #Get current density - linear sweep voltametry
        channel_list = []
        for i in range(num_measurements):
            channel = str(100+i+1) #We add the number of measurements to the index. Go from 101-108
            com_mm.write("channel.setdmm('"+channel+"', dmm.ATTR_MEAS_FUNCTION, dmm.FUNC_4W_RESISTANCE)")
            com_mm.write("beeper.beep(1, "+str(600+i*10)+")") 
            com_mm.write('scan.add("'+channel+'")') 


        #Load all eight channels
        com_mm.write("scan.scancount = scanCount")
        com_mm.write("print(string.format('Loaded scans'))")
        com_mm.write("trigger.model.initiate()")
        com_mm.write("print(string.format('Loaded scans'))") #WHERE DOES THIS GO? THE FUCNTIONS seem to work, but nothing is appearing on here or TSB
        com_mm.write("waitcomplete()")
        ##This is where we output results. Make choice on PRINT vs. save to disk
        #Output results over. 
        com_mm.write("end")
        com_mm.write("endscript")


        com_mm.write(script_name+".run()")
        com_mm.write("W_sweep()")
        com_mm.write(("printbuffer(1, defbuffer1.n, defbuffer1.readings, defbuffer1.channels)"))
        raw_data = com_mm.read()
        time.sleep(15) #need some time to read stuff
        print(raw_data) #This prints to the terminal, but needs a specific 
        filename = input("Write your intended file name.")
        
        #Now we need to save the raw_data as a csv file.
        #output = raw_data.string().split() #Check how the data is split.
        output = raw_data.split() # Debugging.
        with open(f'{filename}.csv', mode = 'w', newline='') as csv_file:
            write = csv.writer(csv_file)
            write.writerow(output)
        
        print(f"Run complete, data written to {filename}.csv")

        return