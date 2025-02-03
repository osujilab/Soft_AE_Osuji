###############################################################################
# Custom MethodScript building for automated/autonomous EmStat Pico measurements
###############################################################################

# ** Likely worth converting to a class definition **

# Clearest solution so far: each time we need a new type of measurement from the Pico, 
# make a new technique definition that is essentially a Python wrapper around an otherwise 
# static MethodScript file, but can flexibly change particular technique parameters. 
# These files will run one at a time when passed to a script provided by PalmSens, and 
# extract data through that as well.
#
# The script will generate/overwrite a file housed in "./scriptbin" that contains the measurement 
# instructions in MethodSCRIPT, as parsed by the instrument.
# 
# What parameters need varying?
# - filename = file name to write to the "scriptbin" directory
# - mux_ch = multiplexer channel (1 thru 16)
# - mVac = Signal amplitude (mV)
# - f_hi = High freq bound (Hz)
# - f_lo = Low freq bound (Hz)
# - npts = Number of points
# - mVdc = DC offset (mV)
# - speed = speed mode: 3 is high (3 default for now)
# - inst_ch = instrument channel (0 default for now)
# - Autorange on/off? (will build in later)

def eis_run_mscrbuild(filename,mux_ch,mVac,f_hi,f_lo,npts,mVdc,inst_ch=0,speed=3):
    
    chan = str(hex(17*(mux_ch-1)))+'i' # channel index shift to select MUX 1 thru 16 
    
    # need to figure out robust filename handling (whether exists or not, don't want to create new one each time)
    # writing custom EIS script to pass to MSCRIPT_FILE_PATH in the EmStat prepackaged section
    f = open(filename, "w") #"a" appends, "w" writes anew, "r" reads 
    f.write("e\n"
            "set_gpio_cfg 0x3FFi 1\n" #proper GPIO config for MUX interfacing
            "set_gpio 0x11i\n" #arbitrarily calling the second MUX channel 
            "var f\nvar r\nvar j\n" #initializing freq, z_real, z_im containers
            f"set_pgstat_chan {inst_ch}\n"
            f"set_pgstat_mode {speed}\n"
            "set_autoranging ba 1p 1\n"
            "set_autoranging ab 1p 1\n"
            "cell_on\n"
            f"set_gpio {chan}\n"
            "wait 10m \n"
            f"meas_loop_eis f r j {mVac}m {f_hi} {f_lo} {npts} {mVdc}m\n"
            " pck_start\n pck_add f\n pck_add r\n pck_add j\n pck_end\nendloop\n"
            "on_finished:\n"
            "cell_off\n\n")
    f.close()


# Linear sweep voltammetry (LSV) script to run as a check of whether this works

def lsv_run_mscrbuild(filename,mux_ch):
    
    chan = str(hex(17*(mux_ch-1)))+'i' # channel index shift to select MUX 1 thru 16 
    
    f = open(filename, "w")
    f.write("e\n"
            "set_gpio_cfg 0x3FFi 1\n" #proper GPIO config for MUX interfacing
            "set_gpio 0x11i\n" #arbitrarily calling the second MUX channel, first one is 0x00i
            "var i\nvar c\nvar p\n" #initializing MUX channel index, current, and potential
            "store_var i 0i aa\n" #set starting MUX channel value (set variable i to 0i (which means 0,"i" for integer, aa is variable type (unknown))
            "set_pgstat_chan 0\n"
            "set_pgstat_mode 2\n"
            "set_max_bandwidth 400\n"
            "set_pot_range -1 1\n"
            "set_cr 1m\n"
            "set_autoranging 10u 1m\n"
            "cell_on\n"
            f"set_gpio {chan}\n"
            "set_e -1000m\n"
            "wait 100m\n"
            "meas_loop_lsv p c -1 1 10m 1\n" # currently set to a fixed sweep from -1 to +1 V in 10mV increments.
            " pck_start\n pck_add p\n pck_add c\n pck_end\nendloop\n"
            "on_finished:\n"
            "cell_off\n\n")
    f.close()
