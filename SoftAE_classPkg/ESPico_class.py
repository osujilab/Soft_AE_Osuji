# Initializes ESPico functionality

# Standard library imports
import datetime
import logging
import os
import os.path
import sys

#os.system("pip3 install -r ESPico_requirements.txt") #in case dependencies need reinstalling

import matplotlib.pyplot as plt
import numpy as np

#sys.path.append('./pspython')

# Local imports
import palmsens.instrument
import palmsens.mscript
import palmsens.serial

import pspython.pspydata
import pspython.pspyfiles
import pspython.pspyinstruments
import pspython.pspymethods

from PalmSens import CurrentRange
from PalmSens import CurrentRanges
from PalmSens import Method
from PalmSens.Techniques import Impedance

import SoftAE_ESPico_mscr_library as mscr

class ESPico:

    def __init__(self,name,port):
        self.name = name
        self.port = port
        
    def sendscript_getdata(self,mscrpath,outdir,chan):
             
        with palmsens.serial.Serial(self.port, 1) as comm:
            print(f"Establishing {self.name} connection.")
            device = palmsens.instrument.Instrument(comm)
            device_type = device.get_device_type()
            #LOG.info('Connected to %s.', device_type) #uncomment to enable logging

            # Read and send the MethodSCRIPT file.
            #LOG.info('Sending MethodSCRIPT.') #uncomment to enable logging
            print(f"Sending script to run on channel {chan}...")
            device.send_script(mscrpath) #this is the command to port with the temp file

            # Read the result lines.
            #LOG.info('Waiting for results.') #uncomment to enable logging
            result_lines = device.readlines_until_end()
        
            os.makedirs(outdir, exist_ok=True)
            result_file_name = datetime.datetime.now().strftime('ms_plot_%Y%m%d-%H%M%S.txt')
            result_file_path = os.path.join(outdir, result_file_name)
            with open(result_file_path, 'wt', encoding='ascii') as file:
                file.writelines(result_lines)
            rawdata = palmsens.mscript.parse_result_lines(result_lines)

            print('Data loaded.')
        return rawdata
    

    def eis_dataplot(self,rawdata,ch): #plot incoming EIS raw data from a single channel
        AX1_COLOR = 'red'
        AX2_COLOR = 'blue'
        f = palmsens.mscript.get_values_by_column(rawdata, 0)
        zreal = palmsens.mscript.get_values_by_column(rawdata, 1)
        zimg = palmsens.mscript.get_values_by_column(rawdata, 2)
        z_complex = zreal + 1j * zimg
        phase = np.angle(z_complex,deg=True)
        z = np.abs(z_complex)

        zimg = -zimg

        # Plot the results.
        # Show the Nyquist plot as figure 1.
        plt.figure(1)
        plt.loglog(zreal, zimg)
        plt.title(f"Nyquist plot, CH{str(ch)}")
        plt.axis('equal')
        plt.grid()
        plt.xlabel("Z'")
        plt.ylabel("-Z''")
        # plt.savefig('nyquist_plot.png')

        # Show the Bode plot as dual y axis (sharing the same x axis).
        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()

        ax1.set_xlabel('Frequency (Hz)')
        ax1.grid(which='major', axis='x', linestyle='--', linewidth=0.5, alpha=0.5)
        ax1.set_ylabel('Z', color=AX1_COLOR)
        # Make x axis logarithmic.
        ax1.loglog(f, z, color=AX1_COLOR)
        # Show ticks.
        ax1.tick_params(axis='y', labelcolor=AX1_COLOR)
        # Turn on the minor ticks, which are required for the minor grid.
        ax1.minorticks_on()
        # Customize the major grid.
        ax1.grid(which='major', axis='y', linestyle='--', linewidth=0.5, alpha=0.5, color=AX1_COLOR)

        # We already set the x label with ax1.
        ax2.set_ylabel('-Phase (degrees)', color=AX2_COLOR)
        ax2.semilogx(f, phase, color=AX2_COLOR)
        ax2.tick_params(axis='y', labelcolor=AX2_COLOR)
        ax2.minorticks_on()
        ax2.grid(which='major', axis='y', linestyle='--', linewidth=0.5, alpha=0.5, color=AX2_COLOR)

        fig.suptitle(f"Bode plot, CH{str(ch)}")
        fig.tight_layout()
        plt.show()

        alldata = [f, z, phase]

        return alldata

    def lsv_dataplot(self,data,ch): #plot incoming linear sweep voltammetry raw data from a single channel
        appl_pot = palmsens.mscript.get_values_by_column(data, 0)
        Imeas = palmsens.mscript.get_values_by_column(data, 1)
        
        plt.figure(1)
        plt.plot(appl_pot, Imeas)
        plt.title(f'LSV plot, CH{ch}')
        plt.axis('tight')
        plt.grid()
        plt.xlabel("V$_{applied}$ (V)")
        plt.ylabel("I$_{meas}$ (A)")
        plt.show()

        slope = (appl_pot[-1]-appl_pot[0])/(Imeas[-1]-Imeas[0]) #using endpoints

        print(f'Resistance: {round(slope,2)} Ohm') #testing on resistors

    def eis_datafromfile(file): # read data from a saved file containing hex ESPico data packets 
        SMALL_SIZE = 12
        MEDIUM_SIZE = 14
        BIGGER_SIZE = 16

        plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
        plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
        plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
        plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
        plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
        plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
        plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
        
        with open(file) as f:
            result_lines = f.readlines()
        rawdata = palmsens.mscript.parse_result_lines(result_lines)

        AX1_COLOR = 'red'
        AX2_COLOR = 'blue'
        f = palmsens.mscript.get_values_by_column(rawdata, 0)
        zreal = palmsens.mscript.get_values_by_column(rawdata, 1)
        zimg = palmsens.mscript.get_values_by_column(rawdata, 2)
        z_complex = zreal + 1j * zimg
        phase = np.angle(z_complex,deg=True)
        z = np.abs(z_complex)

        zimg = -zimg

        # Plot the results.
        # Show the Nyquist plot as figure 1.
        plt.figure(1)
        plt.plot(zreal, zimg)
        plt.title("Nyquist plot")
        plt.axis('tight')
        plt.grid()
        plt.xlabel("Z'")
        plt.ylabel("-Z''")
        # plt.savefig('nyquist_plot.png')

        # Show the Bode plot as dual y axis (sharing the same x axis).
        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()

        ax1.set_xlabel('Frequency (Hz)')
        ax1.grid(which='major', axis='x', linestyle='--', linewidth=0.5, alpha=0.5)
        ax1.set_ylabel('Z', color=AX1_COLOR)
        # Make x axis logarithmic.
        ax1.loglog(f, z, color=AX1_COLOR)
        # Show ticks.
        ax1.tick_params(axis='y', labelcolor=AX1_COLOR)
        # Turn on the minor ticks, which are required for the minor grid.
        ax1.minorticks_on()
        # Customize the major grid.
        ax1.grid(which='major', axis='y', linestyle='--', linewidth=0.5, alpha=0.5, color=AX1_COLOR)

        # We already set the x label with ax1.
        ax2.set_ylabel('-Phase (degrees)', color=AX2_COLOR)
        ax2.semilogx(f, phase, color=AX2_COLOR)
        ax2.tick_params(axis='y', labelcolor=AX2_COLOR)
        ax2.minorticks_on()
        ax2.grid(which='major', axis='y', linestyle='--', linewidth=0.5, alpha=0.5, color=AX2_COLOR)

        fig.suptitle("Bode plot")
        fig.tight_layout()
        plt.show()

        alldata = [f, z, phase]

        return alldata