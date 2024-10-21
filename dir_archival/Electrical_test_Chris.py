### This is code modified from Pavel's initial electrical test code.
##Author: Chris
## This is a playground for trying out random connections and useful ideas with electrical testing on Keithley DAQ6510

from cgi import test
from optparse import Values
from sqlite3 import Row
from time import time
import tkinter as tk
from turtle import width
import pyvisa
import time 
# import keyboard
import time
import cv2
from PIL import Image, ImageTk
from webbrowser import get
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import threading as th
import minimalmodbus
from skopt import Optimizer
from skopt.plots import plot_objective
from skopt.plots import plot_evaluations
# from simple_pid import PID
import os
rm = pyvisa.ResourceManager()
print(rm.list_resources()) 





# Initialize Keithley DAQ6510 Multimeter:
com_mm = rm.open_resource('USB0::0x05E6::0x6510::04433485::INSTR')
com_mm.clear() # We need to clear before running a program, otherwise things will go poorly.
com_mm.write("*IDN?\n")
print(com_mm.read())

com_mm.clear()
com_mm.close()
com_mm = rm.open_resource('USB0::0x05E6::0x6510::04433485::INSTR')

#Attempt writing SCPI function:


#Attempt writing TSP functions and controlling Keithley
#the script below works, but cannot delete scripts from the multimeter...
script_name = "testscript"

com_mm.write("loadscript "+ script_name)

com_mm.write("function myBeepFunction(duration,freq)")

com_mm.write("beeper.beep(duration, freq)")

com_mm.write("end")
com_mm.write("endscript")



com_mm.write(script_name+".run()")
com_mm.write("myBeepFunction(1,1200)")
time.sleep(0.1)
com_mm.write("myBeepFunction(1,800)")
time