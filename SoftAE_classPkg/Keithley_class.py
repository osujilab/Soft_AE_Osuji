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
        #global com_mm #This fixed the continuous opening - global. 
        #Make sure not to define com_mm in any other function.
        self.com_mm = rm.open_resource(ID)
        #global 

    def reset_func_write(self):
        #Attempt writing SCPI function: - write function to reset scripts on multimeter
        script_name = "destroy"
        self.com_mm.write("loadscript "+ script_name)

        #   Attempt writing TSP functions and controlling Keithley
        #the script below works, but cannot delete scripts from the multimeter...
        self.com_mm.write("reset()")
        self.com_mm.write("beeper.beep(0.1, 600)")
        self.com_mm.write("script.delete(string.format('W_sweep'))")
        self.com_mm.write("endscript")

    def reset_func_read(self):
        self.com_mm.write("destroy.run()")

    def elec_export_csv(self,rawdata,filename):
        
        output = rawdata.split(',') #Check how the data is split.

        with open(f'{filename}.csv', mode = 'w', newline='') as csv_file:
            writed = csv.writer(csv_file)
            writed.writerow(output)
            
        print(f"Data written to {filename}.csv")

    def checkBuffer(self):
         self.com_mm.write(("printbuffer(1, defbuffer1.n, defbuffer1.readings, defbuffer1.channels)"))
         time.sleep(1)
         result = self.com_mm.read()
         time.sleep(1)
         print(f'Current buffer readout: {str(result)}')

         return result

    def singleCh_measure(self, ch, scanCount):
        """
        Function takes arbitrary measurements from a single channel.

        ## STILL NEED TO FIGURE OUT TUNABLE ACQUISITION INTERVAL ## 

        1. Initialize DAQ code.
        2. Measure on 8 channels.
        3. Output each channel into CSV
        
        returns a "result" datastring in comma delimited format of <measurement1>,<channel ID>, <m2>, <chID>, ....

        scanCount = number of repeat scan cycles
        sampleCount = number of samples to measure
        """
        #Section 1, write the DAQ communication code
        ##Note - we should decide if we initialize in here too. I say no and make a startup function.
        self.reset_func_write()
        self.reset_func_read()

        time.sleep(0.5)

        script_name = "W_sweep"
        self.com_mm.write("loadscript "+ script_name)
        self.com_mm.write("function W_sweep()")
        #Load initial parameters
        self.com_mm.write("reset()")
        self.com_mm.write(f"scanCount={scanCount}")
        self.com_mm.write(f"sampleCount=1")
        self.com_mm.write("defbuffer1.capacity = scanCount * sampleCount")
        #Set up each channel measurement, we want to sweep voltage, measure current
        #Get current density - linear sweep voltametry

        channel = str(100+ch) #We add the number of measurements to the index. Currently goes from 101-108, will eventually go to 110.
        self.com_mm.write("channel.setdmm('"+channel+"', dmm.ATTR_MEAS_FUNCTION, dmm.FUNC_4W_RESISTANCE)")
        #self.com_mm.write("beeper.beep(0.05, "+str(600+i*10)+")") 
        self.com_mm.write('scan.add("'+channel+'")') 

        #Load all eight channels
        self.com_mm.write("scan.scancount = scanCount")
        #com_mm.write("print(string.format('Loaded scans'))")
        self.com_mm.write("trigger.model.initiate()")
        #com_mm.write("print(string.format('Loaded scans'))") #WHERE DOES THIS GO? THE FUCNTIONS seem to work, but nothing is appearing on here or TSB
        self.com_mm.write("waitcomplete()")
        
        ##This is where we output results. Make choice on PRINT vs. save to disk
        #Output results over. 
        self.com_mm.write("end")
        self.com_mm.write("endscript")

        self.com_mm.write(script_name+".run()")
        self.com_mm.write("W_sweep()")

        time.sleep(0.2*scanCount) # 0.2 s: shortest time that a single channel meas can take. 0.1 does NOT work.
                
        self.com_mm.write(("printbuffer(1, defbuffer1.n, defbuffer1.readings, defbuffer1.channels)"))
        time.sleep(0.2)
        result = self.com_mm.read()
        time.sleep(0.2)
        print(f'Raw data: {str(result)}')

        return result

    def multi_measure(self, channel_list, scanCount):
        """
        Function takes number of AE measurements, measures set of results.
        1. Initialize DAQ code.
        2. Measure on 8 channels.
        3. Output each channel into CSV
        
        returns a "result" datastring in comma delimited format of <measurement1>,<channel ID>, <m2>, <chID>, ....

        scanCount = number of repeat scan cycles
        sampleCount = number of samples to measure
        """
        #Section 1, write the DAQ communication code
        ##Note - we should decide if we initialize in here too. I say no and make a startup function.
        self.reset_func_write()
        self.reset_func_read()

        time.sleep(1)

        script_name = "W_sweep"
        self.com_mm.write("loadscript "+ script_name)
        self.com_mm.write("function W_sweep()")
        #Load initial parameters
        self.com_mm.write("reset()")
        self.com_mm.write(f"scanCount={scanCount}")
        self.com_mm.write(f"sampleCount={len(channel_list)}")
        self.com_mm.write("defbuffer1.capacity = scanCount * sampleCount")
        #Set up each channel measurement, we want to sweep voltage, measure current
        #Get current density - linear sweep voltametry

        for i in range(len(channel_list)):
            channel = str(100+(channel_list[i])) #We add the number of measurements to the index. Currently goes from 101-108, will eventually go to 110.
            self.com_mm.write("channel.setdmm('"+channel+"', dmm.ATTR_MEAS_FUNCTION, dmm.FUNC_4W_RESISTANCE)")
            #self.com_mm.write("beeper.beep(0.05, "+str(600+i*10)+")") 
            self.com_mm.write('scan.add("'+channel+'")') 

        #Load all eight channels
        self.com_mm.write("scan.scancount = scanCount")
        #com_mm.write("print(string.format('Loaded scans'))")
        self.com_mm.write("trigger.model.initiate()")
        #com_mm.write("print(string.format('Loaded scans'))") #WHERE DOES THIS GO? THE FUCNTIONS seem to work, but nothing is appearing on here or TSB
        self.com_mm.write("waitcomplete()")
        
        ##This is where we output results. Make choice on PRINT vs. save to disk
        #Output results over. 
        self.com_mm.write("end")
        self.com_mm.write("endscript")

        self.com_mm.write(script_name+".run()")
        self.com_mm.write("W_sweep()")

        #time.sleep(0.2) # 0.2 s: shortest time that a single channel meas can take. 0.1 does NOT work.
        time.sleep(0.3*(scanCount*len(channel_list)))
        
        self.com_mm.write(("printbuffer(1, defbuffer1.n, defbuffer1.readings, defbuffer1.channels)"))
        time.sleep(0.5)
        result = self.com_mm.read()
        time.sleep(1)
        print(f'Raw data: {str(result)}')

        return result
    
