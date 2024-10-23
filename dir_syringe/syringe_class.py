#This python code is designed to initialize communication with a
#syringe, and print communcations status, as well as control flow.

#Import packages
import pyvisa
import time
from stage_class import stage
rm = pyvisa.ResourceManager()
#We want each stage to be an object with attributes and functions
#Attributes of stage:
#1. Flow rate of syringe
#2. The port it is connected to.
#3. Current syringe position
#Currently, we currently have two active ports for syringes (10/22/2024)

class syringe:


    def __init__(self, port, baud, diameter):
        self.port = port
        self.baud = baud
        self.diameter = diameter
        global com_syr
        #This fixed the continuous opening - global. 
        #Make sure not to define com_pxpy in any other function.
        com_syr = rm.open_resource(self.port)
        print(f"Communication established for syringe pumps on port {port}") 

    def single_pump(self, res_vol, ID, rate, dispense_vol):
        com_syr.write(f"{ID} svolume {res_vol} ml")
        sy_dia = self.diameter
        time.sleep(0.1)
        #need comm language of pump? - harvard apparatus mmanual pg 80-100
        com_syr.write(str(ID) + 'diameter ' + str(float(sy_dia)))
        time.sleep(0.1)

        com_syr.write(str(ID) + 'irate ' + str(float(rate)) + ' ul/min')
        time.sleep(0.1)

        com_syr.write(str(ID) + 'tvolume ' + str(float(dispense_vol)) + ' ul')
        time.sleep(0.1)
    
    def syr_end(self):
        #rm = pyvisa.ResourceManager()
        rm.close()
        print("Session closed.")

    def flush(self):
        """This function goes through a flushing method"""


##TEST##
joe = syringe('ASRL4::INSTR', 115200, 12.03)
joe.syr_end()
