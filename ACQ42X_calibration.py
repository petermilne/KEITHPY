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
has_gains = 0
run_count_top = 1


print "\nAI UUT = "+ai_uut+":"+ai_site
print "AO UUT = "+ao_uut+":"+ao_site

raw_input('\033[1m'+"Is this correct? If so Press Enter to continue..."+'\033[0m')
card = sys.argv[1]


if card == 'acq420' or card == 'acq425' :
    has_gains = 1
    keith_func.set_GAIN_all(0)
    run_count_top = 4

############ Set output filename and open for CSV writing #########
command_str = ai_uut+":"+ai_site+":SERIAL";card_serial = caget(command_str)
command_str = ai_uut+":"+ai_site+":MODEL";model = caget(command_str)
command_str = ai_uut+":"+ai_site+":NCHAN";nchan = caget(command_str)
command_str = ai_uut+":1:INTCLK_HZ";sample_rate = str(caget(command_str))
sample_rate_str = str(sample_rate)+" Hz"
command_str = ai_uut+":SYS:VERSION:SW";firm_rev = str(caget(command_str))
command_str = ai_uut+":SYS:VERSION:FPGA";fpga_rev = str(caget(command_str))
amb_temp = keith_func.getAmbTemp();temp_str = str(amb_temp)
timestamp = str(time.strftime("%Y%m%d_%H%M%S"))
print "Temperature @ run : "+temp_str+" C"

filename = "./results/"+card_serial

###################################################################
start = time.time()

keith_func.set_TRG(0)
keith_func.set_SPAN_all(3)
keith_func.set_AO_all(0)


#voltages = np.array([ np.arange(-10,10.5,0.5), np.arange(-5,5.25,0.25), np.arange(-2.5,2.625,0.125), np.arange(-1.25,1.3125,0.0625) ])   # Specify voltages to loop through, this notation is broken as a consequence of there being no software catch for +ve FS. This may be fixed in the future.
voltages = np.array([ np.arange(-10,20,10), np.arange(-5,10,5), np.arange(-2.5,5,2.5), np.arange(-1.25,2.5,1.25)])#, np.arange(-2.5,2.625,0.125), np.arange(-1.25,1.3125,0.0625) ])   # Specify voltages to loop through, this notation is broken as a consequence of there being no software catch for +ve FS. This may be fixed in the future.
for run in range(0,run_count_top):
    
    # Create filenames and open CSV
    if has_gains == 1 :
        csv_filename = filename+"_gain"+str(run)+".csv"
    else :
        csv_filename = filename+".csv"
    print csv_filename
    result_file = open(csv_filename,'wb')
    csv_write = csv.writer(result_file)
    
    # Create header for CSV
    channel_header  = ['CH{0:0>2}'.format(i) for i in range(1, nchan+1)]
    channel_header.append('Supplied Voltage')
    csv_write.writerow(channel_header)
    
    # Set gains and begin streaming, 3 seconds of settling time
    if has_gains == 1 : keith_func.set_GAIN_all(run)
    keith_func.start_stream()
    time.sleep(3)
    
    code_array = []
    
    ############ Begin setting AO voltages and reading back from Keithley and AI Card #########
    for i in range (0, len(voltages[run])):
        v_str = str(voltages[run][i])
        print "V = "+v_str+"V"
        code_array.append([])   # Add another sublist to master list
        keith_func.set_AO_all(voltages[run][i])   # Set AO on current channel
        time.sleep(4)
        
        for channel in range (1,nchan+1):
            
            code_array[i].append(keith_func.get43Xcode(channel))
                    
            # Record DAC Code
            if channel == nchan: code_array[i].append(keith_func.getKVolts(1,nchan)); print code_array[i]
        
        csv_write.writerow(code_array[i])  # Write to CSV, format as below
    
    # Return AO to 0V, back to default gains, stop streaming, close CSV file
    keith_func.set_AO_all(0)
    if has_gains == 1 : keith_func.set_GAIN_all(0)
    keith_func.stop_stream()
    result_file.close()

# Call XML generation which in turn calls octave. The eventual output is an XML file describing calibration coefficients for a whole board
process_cal_data.process(timestamp,model,nchan,card_serial,amb_temp,sample_rate_str,firm_rev,fpga_rev)

print
end = time.time()
print end - start
print timestamp
print ai_uut
print "Temperature @ run : "+temp_str+" C"

