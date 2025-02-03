# Multichannel testing

# To do: formalize data storage in a reasonable way to flexibly collect and store.
# Currently, sendscript_getdata can return a single run, and this can # be stored in any general data structure.

#the below line loads the Pico class AND our custom MethodScript library (mscr)
import ESPico_class as EP
import SoftAE_ESPico_mscr_library as mscr

port = EP.palmsens.serial.auto_detect_port() # find the instrument (only one attached)
p = EP.ESPico('Pico1',port) # name and specify the port of this instance of ESPico class.

chlist = [] # Define multiplexer channel list
# if wanting all samples within a range use the below: 
for i in range(2,4): #range is exclusive of end index: range(m,n) is m to n-1
    chlist.append(i)

plotlist = [2,3] #if you want to selectively see the data

scriptPath = 'scripts/testing.mscr'
outPath = 'output'

# multichannel data recall and selective plotting
for ch in chlist:
    #mscr.eis_run_mscrbuild(scriptPath,ch,10,20000,100,50,0) # write custom MethodScript
    mscr.lsv_run_mscrbuild(scriptPath,ch)
    c = p.sendscript_getdata(scriptPath,outPath,ch)
    if ch in plotlist:
        p.lsv_dataplot(c,ch)
        #p.eis_dataplot(c,ch)

#quit() # break in the code to test switching between channels


