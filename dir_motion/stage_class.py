#This python code is designed to initialize communication withthe x/y
#motion stage, and print communcations status.

#Import packages
import pyvisa
import time
import numpy as np
rm = pyvisa.ResourceManager()

#We want each stage to be an object with attributes and functions
#Attributes of stage:
#1. Direction it is design to move in (x/y, x/y/z)
#2. The port it is connected to.
#3. The location.
#Currently, our setup is only x/y and is connected to a known port.
###
#We don't want any dependencies on other devices in this file.
#Syringe and AE setup will need this file.
###

#Ideally people can generalize this.
class stage:


    def __init__(self, port, baud):
        self.port = port
        self.baud = baud #We know this is 921600 for our stage.
        global com_pxpy #This fixed the continuous opening - global. 
        #Make sure not to define com_pxpy in any other function.
        com_pxpy = rm.open_resource(self.port)
        #global 

    def stage_init(self):
        #Import packages, run __init__, now set_baud_rate
        com_pxpy.baud_rate = self.baud #Fixed, why?
        print(f"Communication established for linear stage on port {self.port}")

    def live_position(self):
        #Comm established, now print live position        
        #Turns on Motion Controller
        com_pxpy.write('1MO')
        com_pxpy.write('2MO')
        live_position_x_t = com_pxpy.query_ascii_values('1TP?')
        live_position_x = ''.join(str(element) for element in live_position_x_t)
        live_position_y_t = com_pxpy.query_ascii_values('2TP?')
        live_position_y = ''.join(str(element) for element in live_position_y_t)
        print(f'The current stage position is (x,y): ({live_position_x},{live_position_y})')    
    
    def stage_end(self):
        #rm = pyvisa.ResourceManager()
        rm.close()
        print("Session closed.")

    def move_to(self, x, y):
        """This function takes float input and moves linear stage"""
        x = str(x)
        y = str(y)
        #com_pxpy = stage.open_resource(self)
        com_pxpy.write(f'1PA{x}')
        time.sleep(0.5)              
        com_pxpy.write(f'2PA{y}')
        time.sleep(0.5)
        print(f"Movement completed. Stage is now at (x,y):({x},{y})")

    def array_pos(self, x_list, y_list):
        """If you have an array of positions (i.e. electrode), you can define it here
        THis is if you don't already have an x-y array ready. Good for making new array defs"""
        pos_array = np.array(x_list, y_list)
        return pos_array
        




##TEST##
#jeff = stage('ASRL7::INSTR', 921600)
#print(jeff.port)
#jeff.stage_init()
#jeff.live_position()
#jeff.move_to(-40, -5)
#jeff.live_position()
#jeff.stage_end()