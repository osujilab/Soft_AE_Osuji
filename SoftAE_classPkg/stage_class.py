#This python code is designed to initialize communication withthe x/y
#motion stage, and print communcations status.

#Import packages
import pyvisa
import time
import numpy as np
#rm = pyvisa.ResourceManager()
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
    #
    def __init__(self, port, baud):
        self.port = port
        self.baud = baud #We know this is 921600 for our stage.
        global com_pxpy #This fixed the continuous opening - global. 
        #Make sure not to define com_pxpy in any other function.
        self.rm = pyvisa.ResourceManager()
        # com_pxpy = self.rm.open_resource(self.port)
        # self.com_pxpy = com_pxpy
        self.com_pxpy = self.rm.open_resource(self.port)

        
        #global 

    def stage_init(self):
        #Import packages, run __init__, now set_baud_rate
        self.com_pxpy.baud_rate = self.baud #Fixed, why?
        print(f"Communication established for linear stage on port {self.port}")

    def live_position(self, print_flag=0):
        #Comm established, now print live position        
        #Turns on Motion Controller
        self.com_pxpy.baud_rate = self.baud
        self.com_pxpy.write('1MO')
        self.com_pxpy.write('2MO')
        # time.sleep(0.5)
        live_position_x_t = self.com_pxpy.query_ascii_values('1TP?')
        live_position_x = ''.join(str(element) for element in live_position_x_t)
        live_position_y_t = self.com_pxpy.query_ascii_values('2TP?')
        live_position_y = ''.join(str(element) for element in live_position_y_t)
        if print_flag == 1:
            print(f'The current stage position is (x,y): ({live_position_x},{live_position_y})') 

        return (live_position_x, live_position_y)   
    
    def stage_end(self):
        #rm = pyvisa.ResourceManager()
        self.com_pxpy.close()
        print("Session closed.")

    def move_to(self, x, y):
        """This function takes float input and moves linear stage"""
        x = str(x)
        y = str(y)
        self.com_pxpy.baud_rate = self.baud

        #com_pxpy.baud_rate = self.baud
        self.com_pxpy.write(f'1PA{x}')
        time.sleep(0.5)              
        self.com_pxpy.write(f'2PA{y}')
        time.sleep(0.5) 
        #timeout = 0
        self.query_status()
        while self.com_pxpy.query('TS?') != 'P\r\n':
        # R - axis 2 is moving, axis 1 is not #P - nothing happening, #Q - axis 1 moving #S - both moving 
        # From the manual of ESP301 ASCII binary conversion. We want to ensure that we register correct live position
           wait = 3
           print("Moving...")
           time.sleep(wait)
           timeout += wait
           if timeout > 15:
               break
        #print(self.com_pxpy.query('TS?'))
        new_pos_x = self.com_pxpy.query_ascii_values('1TP?') #Want to query live position
        new_pos_y = self.com_pxpy.query_ascii_values('2TP?')
        print(f"Movement completed. Stage is now at (x,y):({new_pos_x},{new_pos_y})")

    def move_by(self, x, y):
        """This function takes float input and moves linear stage by relative units"""
        x = str(x)
        y = str(y)
        self.com_pxpy.baud_rate = self.baud

        #com_pxpy.baud_rate = self.baud
        self.com_pxpy.write(f'1PR{x}')
        time.sleep(0.5)              
        self.com_pxpy.write(f'2PR{y}')
        time.sleep(0.5) 
        
        self.query_status()
        #while self.com_pxpy.query('TS?') != 'P\r\n':
        #R - axis 2 is moving, axis 1 is not #P - nothing happening, #Q - axis 1 moving #S - both moving 
        #From the manual of ESP301 ASCII binary conversion. We want to ensure that we register correct live position
        #    wait = 3
        #    print("Moving...")
        #    time.sleep(wait)
        #    timeout += wait
        #    if timeout > 15:
        #        break
        #print(self.com_pxpy.query('TS?'))
        new_pos_x = self.com_pxpy.query_ascii_values('1TP?') #Want to query live position
        new_pos_y = self.com_pxpy.query_ascii_values('2TP?')
        print(f"Movement completed. Stage is now at (x,y):({new_pos_x},{new_pos_y})")


    def array_pos(self, x_list, y_list):
        """If you have an array of positions (i.e. electrode), you can define it here
        THis is if you don't already have an x-y array ready. Good for making new array defs"""
        pos_array = np.array([x_list, y_list])
        return pos_array
    
    def home_stage(self):
            self.com_pxpy.write('2MO')
            self.com_pxpy.write('1MO')
            self.com_pxpy.write('1OR')
            self.com_pxpy.write('2OR')
            ## self.query_status()
            print("Homing completed.")

    def query_status(self):
        timeout = 0
        while self.com_pxpy.query('TS?') != 'P\r\n':
        #R - axis 2 is moving, axis 1 is not 
        #P - nothing happening, 
        #Q - axis 1 moving 
        #S - both moving 
        #From the manual of ESP301 ASCII binary conversion. 
        #We want to ensure that we register correct live position
            wait = 3 #default = 3
            print("Moving...")
            time.sleep(wait)
            timeout += wait
            if timeout > 15:
                break

        

##TEST##
# jeff = stage('ASRL7::INSTR', 921600)
# print(jeff.port)
# jeff.stage_init()
# jeff.live_position()

# jeff.move_to(-20, -5)
# jeff.live_position()
# jeff.stage_end()