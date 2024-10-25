# Testbed for Soft-AE EmStat Pico capabilities
# First try at formalizing definitions for consistency on GitHub 

# initialize relevant dependencies
# Standard library imports
import datetime
import logging
import os
import os.path
import sys

#os.system("pip3 install -r requirements.txt")

# Third-party imports
import matplotlib.pyplot as plt
import numpy as np

psp_dir = 'C:/Users/pshap/Documents/Penn_Research_local/Soft_AE/EIS_capabilities/EmStatPico_tests/pspython' #Pavel's local dir
#psp_dir = 'C:/Users/Osuji/AppData/Local/Programs/Python/Python311/Scripts/AE_EmStat_test' #SoftAE computer local dir

sys.path.append(psp_dir)

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

sys.path.append("../")
import SoftAE_ESPico_mscr_library as mscr

