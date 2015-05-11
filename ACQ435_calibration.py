#!/usr/bin/python

import sys;import time;import csv;import scipy
import numpy as np
import epics;from epics import caget, caput
import keith_func
import global_uut_settings
import matplotlib.pyplot as plt

ai_uut = global_uut_settings.ai_uut
ao_uut = global_uut_settings.ao_uut
ai_site = global_uut_settings.ai_site
ao_site = global_uut_settings.ao_site

print sys.argv[0]
#print sys.argv[1]

nchan = 32

############ Set output filename and open for CSV writing #########
command_str = ai_uut+":"+ai_site+":SERIAL"
card_serial = caget(command_str)
timestamp = time.strftime("%Y%m%d_%H%M")
#filename = "./results/results_"+timestamp+".csv"
filename = "./results/"+card_serial+".csv"
result_file = open(filename,'wb')
csv_write = csv.writer(result_file)
#Create header for CSV
channel_header  = ['CH{0:0>2}'.format(i) for i in range(1, nchan+1)]
channel_header.append('Supplied Voltage')

csv_write.writerow(channel_header)

###################################################################
start = time.time()

keith_func.set_TRG(0)
keith_func.set_SPAN_all(3)
keith_func.set_AO_all(0)
time.sleep(3)

#voltages = np.arange(-10,10.5,0.5)   # Specify voltages to loop through, this notation is broken as a consequence of there being no software catch for +ve FS. This may be fixed in the future.
voltages = [-10,-9.5,-9,-8.5,-8,-7.5,-7,-6.5,-6,-5.5,-5,-4.5,-4,-3.5,-3,-2.5,-2,-1.5,-1,-0.5,0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,9.999]   # Specify voltages to loop through
code_array = []
#meas_volts = []

############ Begin setting AO voltages and reading back from Keithley and ACQ435 #########
for i in range (0, len(voltages)):
    v_str = str(voltages[i])
    print "V = "+v_str+"V"
    code_array.append([])   # Add another sublist to master list
    keith_func.set_AO_all(voltages[i])   # Set AO on current channel
    time.sleep(4)
    
    for channel in range (1,nchan+1):
        
        code_array[i].append(keith_func.get435code(channel))
                
        # Record DAC Code
        if channel == nchan: code_array[i].append(keith_func.getKVolts(1,nchan)); print code_array[i]
    
    csv_write.writerow(code_array[i])  # Write to CSV, format as below

print
end = time.time()
print end - start

keith_func.set_AO_all(0)
