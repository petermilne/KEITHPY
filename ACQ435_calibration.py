#!/usr/bin/python

import sys;import time;import csv;import scipy
import numpy as np
import epics;from epics import caget, caput
import keith_func
import process_cal_data
import global_uut_settings
import matplotlib.pyplot as plt

ai_uut = global_uut_settings.ai_uut
ao_uut = global_uut_settings.ao_uut
ai_site = global_uut_settings.ai_site
ao_site = global_uut_settings.ao_site


print "\nAI UUT = "+ai_uut+":"+ai_site
print "AO UUT = "+ao_uut+":"+ao_site

raw_input('\033[1m'+"Is this correct? If so Press Enter to continue..."+'\033[0m')

#print sys.argv[0]
#print sys.argv[1]
card = sys.argv[1]

nchan = 32

############ Set output filename and open for CSV writing #########
command_str = ai_uut+":"+ai_site+":SERIAL";card_serial = caget(command_str)
command_str = ai_uut+":"+ai_site+":MODEL";model = caget(command_str)
command_str = ai_uut+":1:ACQ43X_SAMPLE_RATE";sample_rate = str(caget(command_str))
command_str = ai_uut+":SYS:VERSION:SW";firm_rev = str(caget(command_str))
command_str = ai_uut+":SYS:VERSION:FPGA";fpga_rev = str(caget(command_str))
amb_temp = keith_func.getAmbTemp();temp_str = str(amb_temp)
timestamp = str(time.strftime("%Y%m%d_%H%M%S"))
print "Temperature @ run : "+temp_str+" C"

#filename = "./results/results_"+timestamp+".csv"
filename = "./results/"+card_serial
# csv_filename = filename+".csv"
# result_file = open(csv_filename,'wb')
# csv_write = csv.writer(result_file)
# #Create header for CSV
# channel_header  = ['CH{0:0>2}'.format(i) for i in range(1, nchan+1)]
# channel_header.append('Supplied Voltage')

# csv_write.writerow(channel_header)

###################################################################
start = time.time()

if card == 'acq435':
    for runs in range(0,2):
        if runs == 0:
            #Set hi-res mode first
            keith_func.set_ACQ43X_sample_rate(30000)
            csv_filename = filename+"_hires.csv"
            result_file = open(csv_filename,'wb')
            csv_write = csv.writer(result_file)
        elif runs == 1:
            #Set hi-res mode first
            keith_func.set_ACQ43X_sample_rate(80000)
            csv_filename = filename+"_hispeed.csv"
            

        result_file = open(csv_filename,'wb')
        csv_write = csv.writer(result_file)
        #Create header for CSV
        channel_header  = ['CH{0:0>2}'.format(i) for i in range(1, nchan+1)]
        channel_header.append('Supplied Voltage')
        csv_write.writerow(channel_header)
        
        keith_func.set_TRG(0)
        keith_func.set_SPAN_all(3)
        keith_func.set_AO_all(0)
        keith_func.start_stream()
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
        
        keith_func.set_AO_all(0)
        keith_func.stop_stream()

# Call XML generation which in turn calls octave. The eventual output is an XML file describing calibration coefficients for a whole board
process_cal_data.process(timestamp,model,card_serial,amb_temp,'30/80 kHz',firm_rev,fpga_rev)

print
end = time.time()
print end - start
print timestamp
print ai_uut
print "Temperature @ run : "+temp_str+" C"

