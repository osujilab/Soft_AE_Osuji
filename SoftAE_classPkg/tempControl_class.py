# Defining a Temperature control object

#29 Oct 2024, Pavel Shapturenka

# As of Oct 2024 the Soft-AE stage temp controller is a Novus N1040, using MODBUS for comms.
# A NI cDAQ unit is used to monitor local surface temperature, with many channels to expand temperature measurement.

import minimalmodbus
import time
import numpy as np
import nidaqmx
import nidaqmx.constants
import matplotlib.animation as ani
import matplotlib.pyplot as plt

class tempControl:

    def __init__(self,name,port,baud,reg_sp,reg_pv):
        self.name = name #identifier in case of scaleup later
        self.port = port # "com6" currently for Novus TC
        self.baud = baud # 115200 for Omega and Novus T controllers
        self.reg_sp = reg_sp # setpoint register, 0 for Novus
        self.reg_pv = reg_pv # process variable register. 1 for Novus
        
        global com_hot
        com_hot = minimalmodbus.Instrument(self.port, 1, minimalmodbus.MODE_RTU)
        com_hot.serial.baudrate = self.baud
        com_hot.close_port_after_each_call= True 

    def get_sp(self):
        return com_hot.read_register(self.reg_sp)/10 # div by 10: Novus oddity wherein decimals do not exist

    def get_pv(self):
             return com_hot.read_register(self.reg_pv)/10 
    
    def get_pv_surf(self):
        with nidaqmx.Task() as task:
            task.ai_channels.add_ai_thrmcpl_chan("cDAQ1Mod1/ai0",min_val=0.0, max_val=100.0,cjc_source=nidaqmx.constants.CJCSource(10200))
            return task.read()

    def write_sp(self,T_SP, print_flag=1):
        cur_SP = self.get_sp()
        com_hot.write_register(self.reg_sp,T_SP*10)
        if print_flag == 1:
            print(f"{self.name} setpoint T changed from {cur_SP} \N{DEGREE SIGN}C to {T_SP*1.0} \N{DEGREE SIGN}C.")

    def wait(self,within):
        # within: acceptable absolute degrees around target to proceed
        # band: (currently not in use): percentage range
        # while abs(self.get_sp()-self.get_pv())/self.get_pv() > band:
        while abs(self.get_sp()-self.get_pv()) > within:
            time.sleep(20)

    def ramp_linear(self,T_start,T_end,t_span,up_int,print_flag=1):
        # Simple temperature ramp script (holds everything else up while running) -- move to tempControl class
        # (need to multi-thread, or insert tasks inside as nested loops if we want other things to run concurrently.)

        # T_start: start temp in C to one decimal precision
        # T_end
        # t_span: seconds to ramp over
        # up_int: update interval in seconds

        t_vals = np.linspace(0,t_span,int(t_span/up_int)) #time
        T_vals = np.round(np.linspace(T_start,T_end,int(t_span/up_int)),1) #temp

        t_0 = time.time()
        wait = 0.5 #wait time in seconds, 0.02 is too small

        for i,t_pt in enumerate(t_vals): #waits for proper time to change to new set point
            is_time = False
            while not is_time:
                time.sleep(wait)
                timenow = time.time()-t_0
                if timenow >= t_pt:
                    #self.wait(0.05) #if being close to set point is necessary to move forward
                    is_time = True
            self.write_sp(T_vals[i])
            if print_flag == 1:
                print(f'Block temp:{str(self.get_pv())}\N{DEGREE SIGN}C, surf temp: {np.round(self.get_pv_surf(),3)}\N{DEGREE SIGN}C')


# Testing/demoing simple initialization and execution

# stageT = tempControl("stage","com5",115200,0,1) #Novus instance

# stageT.get_sp()
# stageT.write_sp(20)
# print(f"Current stage T: {stageT.get_pv()} \N{DEGREE SIGN}C")