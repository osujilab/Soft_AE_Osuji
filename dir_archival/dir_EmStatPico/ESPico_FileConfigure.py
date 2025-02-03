# Multichannel testing

from ESPico_class import *
import SoftAE_ESPico_mscr_library as mscr

port = palmsens.serial.auto_detect_port() # find the instrument

p = ESPico('Pico1',port) # instance of the ESPico class

chlist = [] # Define multiplexer channel list
for i in range(2,4):
    chlist.append(i)

scriptPath = 'scripts/testing.mscr'
outPath = 'output'

for ch in chlist:
    mscr.eis_run_mscrbuild(scriptPath,ch,10,20000,100,50,0)
    c = p.sendscript_getdata(scriptPath,outPath,ch)

quit() # break in the code to test switching between channels


# Data handling below (probably best to do separately anyways, as with methods)
f = palmsens.mscript.get_values_by_column(c, 0)
zreal = palmsens.mscript.get_values_by_column(c, 1)
zimg = palmsens.mscript.get_values_by_column(c, 2)
z_complex = zreal + 1j * zimg
phase = np.angle(z_complex,deg=True)
z = np.abs(z_complex)

zimg = -zimg

plt.figure(1)
plt.plot(f,z)
plt.show
plt.figure(2)
plt.plot(zreal,zimg)
plt.show

