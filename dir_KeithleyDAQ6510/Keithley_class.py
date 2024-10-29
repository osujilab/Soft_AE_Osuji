###CHRIS JOHNSON###
#This python class is storing a lot of the Keithley code so we don't have to worry about
#pasting it into large AE jupyter notebooks. 

##***WIP***##


#Import packages
import pyvisa
import time
import numpy as np
import os
rm = pyvisa.ResourceManager()
print(rm.list_resources())

# Initialize Keithley DAQ6510 Multimeter:
com_mm.clear()
com_mm.write("*IDN?\n")
print(com_mm.read())

com_mm.clear()
com_mm.close()
com_mm = rm.open_resource('USB0::0x05E6::0x6510::04433485::INSTR')

class Keithley:


    def __init__(self, ID):
        self.ID = ID
        global com_mm #This fixed the continuous opening - global. 
        #Make sure not to define com_pxpy in any other function.
        com_mm = rm.open_resource(ID)
        #global 

    def reset_func(self)
    #Attempt writing SCPI function:
        script_name = "destroy"
        com_mm.write("loadscript "+ script_name)

        #   Attempt writing TSP functions and controlling Keithley
        #the script below works, but cannot delete scripts from the multimeter...
        com_mm.write("reset()")
        com_mm.write("beeper.beep(1, 600)")
        com_mm.write("script.delete(string.format('W_sweep'))")
        com_mm.write("endscript")   

    def