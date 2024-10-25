# Initializes ESPico functionality

# Standard library imports
import datetime
import logging
import os
import os.path
import sys

#os.system("pip3 install -r requirements.txt")

import matplotlib.pyplot as plt
import numpy as np

sys.path.append('./pspython')

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

class ESPico:

    def __init__(self,name,port):
        self.name = name
        self.port = port
        
    def sendscript_getdata(self,mscrpath,outdir,chan):
             
        with palmsens.serial.Serial(self.port, 1) as comm:
            print('Establishing device connection.')
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
            curves = palmsens.mscript.parse_result_lines(result_lines)

            print('Data loaded.')
        return curves
    


