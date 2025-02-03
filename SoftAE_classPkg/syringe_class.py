#This python code is designed to initialize communication with a
#syringe, and print communcations status, as well as control flow.

#Import packages
import pyvisa
import time
import nidaqmx
#from SoftAE_classPkg import stage_class
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
        self.rm = pyvisa.ResourceManager()
        self.instrument = self.rm.open_resource(self.port)
        self.com_syr = self.rm.open_resource(self.port)
        print(f"Communication established for syringe pumps on port {port}")
        global is_up #variable keeping track of syringe head position (up - 1, down - 0)

    def single_pump(self, res_vol, ID, rate, dispense_vol):
        self.com_syr.write(f"{ID} svolume {res_vol} ml")
        sy_dia = self.diameter
        time.sleep(0.1)
        #need comm language of pump? - harvard apparatus mmanual pg 80-100
        self.com_syr.write(str(ID) + 'diameter ' + str(float(sy_dia)))
        print("Registered diameter.")
        time.sleep(0.1)

        self.com_syr.write(str(ID) + 'irate ' + str(float(rate)) + ' ul/min')
        print(f"Will dispense at {rate} ul per min from syringe {ID}")
        time.sleep(0.1)

        self.com_syr.write(str(ID) + 'tvolume ' + str(float(dispense_vol)) + ' ul')
        time.sleep(0.1)
        print(f"will dispense {dispense_vol} ul from syringe {ID}")
        self.com_syr.write(str(ID) + 'irun')
        print("running....")

        #Add probing of status
    
    def head_flip(self):
        with nidaqmx.Task() as task:
                task.do_channels.add_do_chan("Dev1/port0/line0:7")
                flip = [0,1,0]
                for i in flip:
                    task.write(i)
                    time.sleep(0.5)

        if self.is_up == 1:
            self.is_up = 0
        elif self.is_up == 0:
            self.is_up = 1

    def head_check(self):
        is_up_str = input("Is the head retracted? (y/n) (If remote: Use stage_webcam_observe.ipynb to check)")
        if is_up_str == 'n':
            self.is_up = 0
            self.head_flip()
            print("Dispenser head retracted.")
        elif is_up_str == 'y':
            self.is_up = 1
            print("Dispenser head retracted.")
        else:
            print('Invalid entry!')
            return
    
    def head_retract(self):
        try:
            if self.is_up == 0:
                self.head_flip()
        except:
            self.head_check()
            if self.is_up == 0:
                self.head_flip()
        else:
            if self.is_up == 0:
                self.head_flip()

    def head_descend(self):
        try:
            if self.is_up == 1:
                self.head_flip()
        except:
            self.head_check()
            if self.is_up == 1:
                self.head_flip()
        else:
            if self.is_up == 1:
                self.head_flip()

    def syr_end(self):
        #rm = pyvisa.ResourceManager()
        self.rm.close()
        print("Session closed.")

    def Flush_AE(self, flush_volume_0, flush_volume_1, flush_time, DCDG_flush):
        """This function goes through a flushing method for syringes 0-1. 
        Ensure sufficient time allowed for liquid loss"""
        rate_flush_0 = 60 * (flush_volume_0 / flush_time)
        rate_flush_1 = 60 * (flush_volume_1 / flush_time) 
        #flush the piping
        if DCDG_flush == 1:

            single_pump(sy_dia, res_vol, 1, rate_flush_1, flush_volume_1) # type: ignore
            time.sleep(1)

        single_pump(sy_dia, res_vol, 0, rate_flush_0, flush_volume_0) # type: ignore
        time.sleep(0.1)
        time.sleep(flush_time+30)     

##TEST##
#joe = syringe('ASRL4::INSTR', 115200, 12.03)
#joe.syr_end()
#