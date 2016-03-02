
import time;
import scipy; import numpy as np
import epics;from epics import caget, caput
import global_uut_settings

ai_uut = global_uut_settings.ai_uut
ao_uut = global_uut_settings.ao_uut
ai_site = global_uut_settings.ai_site
ao_site = global_uut_settings.ao_site 

def wait_valldone2():
    timeout = True
    t0 = time.time()
    while time.time() - t0 < 30.0:
        time.sleep(1.e-3)
        if caget('KMUX:VALLDONE') == 1:
            timeout = False
            #print '\n{0:-^30}\n{1:-^30}'.format(' SCAN COMPLETE! ',' SCAN RESULTS ')
            break
    if timeout:
        print "TIMED OUT READING FROM KMUX!!!!"

def getKVolts(channel,nchan):
    caput ('KMUX:BEEP', 0)

    # Reset if MUXSCAN changes.
    # Resettting causes a BEEP
    if nchan != caget('KMUX:MUXSCAN'):
        caput('KMUX:RST', 1)

    caput ('KMUX:BEEP', 0)
    caput ('KMUX:MUXSCAN', nchan)

    caput ('KMUX:VALLDONE', 0)
    caput ('KMUX:TRIG', 1)

    wait_valldone2()
    i_str = '{0:0>2}'.format(channel)
    command_str = "KMUX:V"+i_str
    volts = caget(command_str)
    return volts[0]

def getKVolts_all(nchan):
    caput ('KMUX:BEEP', 0)

    # Reset if MUXSCAN changes.
    # Resettting causes a BEEP
    if nchan != caget('KMUX:MUXSCAN'):
        caput('KMUX:RST', 1)

    caput ('KMUX:BEEP', 0)
    caput ('KMUX:MUXSCAN', nchan)

    caput ('KMUX:VALLDONE', 0)
    caput ('KMUX:TRIG', 1)

    wait_valldone2()
    Vall = caget('KMUX:VXX')
    return Vall


def getDacCode(channel):
    dac_code_array = []
    i_str = '{0:0>2}'.format(channel)
    command_str = ao_uut+":"+ao_site+":AO:SLOW_SET:CH:"+i_str+".RVAL"
    dac_code = caget(command_str)
    return dac_code
    

def getDacCode_all(nchan):
    dac_code_array = []
    for i in range (1, nchan+1):
        i_str = '{0:0>2}'.format(i)
        command_str = ao_uut+":"+ao_site+":AO:SLOW_SET:CH:"+i_str+".RVAL"
        dac_code_array.insert(i-1,caget(command_str))
    return dac_code_array

def get43Xcode(channel):
    adc_code_array = []
    scaling_factor = 256
    i_str = '{0:0>2}'.format(channel)
    command_str = ai_uut+":"+ai_site+":AI:WF:"+i_str
    adc_codes = caget(command_str)
    adc_code = int(np.round(scipy.mean(adc_codes),0))
    adc_code_scaled = adc_code / scaling_factor
    return adc_code_scaled
    
def get43Xvolts(channel):
    adc_code_array = []
    scaling_factor = 256
    i_str = '{0:0>2}'.format(channel)
    command_str = ai_uut+":"+ai_site+":AI:WF:"+i_str
    adc_codes = caget(command_str)
    adc_code = int(np.round(scipy.mean(adc_codes),0))
    adc_code_scaled = adc_code / scaling_factor
    vsf = np.divide(20.0,2.0**24)
    adc_voltage = np.multiply(adc_code_scaled,vsf)
    #return adc_voltage
    return adc_code_scaled
    
def get43Xcodes_all(nchan):
    dac_code_array = []
    scaling_factor = 256
    for i in range (1, nchan+1):
        i_str = '{0:0>2}'.format(i)
        command_str = ai_uut+":"+ai_site+":AI:WF:"+i_str
        adc_codes = caget(command_str)
        adc_code = int(np.round(scipy.mean(adc_codes),0))
        adc_code_scaled = adc_code / scaling_factor
        adc_code_array.insert(i-1,adc_code_scaled)
    return adc_code_array
    
def get42Xcode(channel):
    adc_code_array = []
    scaling_factor = 1
    i_str = '{0:0>2}'.format(channel)
    command_str = ai_uut+":"+ai_site+":AI:WF:"+i_str
    adc_codes = caget(command_str)
    adc_code = int(np.round(scipy.mean(adc_codes),0))
    adc_code_scaled = adc_code / scaling_factor
    return adc_code_scaled
    
def get480code(channel):
    adc_code_array = []
    scaling_factor = 1
    i_str = '{0:0>2}'.format(channel)
    command_str = ai_uut+":"+ai_site+":AI:WF:"+i_str
    adc_codes = caget(command_str)
    adc_code = int(np.round(scipy.mean(adc_codes),0))
    adc_code_scaled = adc_code / scaling_factor
    return adc_code_scaled

def set_AO(volts,channel):
    i_str = '{0:0>2}'.format(channel)
    command_str = ao_uut+":"+ao_site+":AO:SLOW_SET:CH:"+i_str
    caput(command_str,volts)

# def set_AO_all(volts,nchan):
    # for i in range (1, nchan+1):
        # i_str = '{0:0>2}'.format(i)
        # command_str = ao_uut+":"+ao_site+":AO:SLOW_SET:CH:"+i_str
        # caput(command_str,volts)
	   
def set_AO_all(volts):
        command_str = ao_uut+":"+ao_site+":AO:SLOW_SET:CH:ALL"
        caput(command_str,volts)


def set_SPAN(channel,span):
    i_str = '{0:0>2}'.format(channel)
    command_str = ao_uut+":"+ao_site+":RANGE:"+i_str
    caput(command_str,span)

def set_SPAN_all(span):
    command_str = ao_uut+":"+ao_site+":RANGE:ALL"
    caput(command_str,span)
    
def set_GAIN_all(gain):
    command_str = ai_uut+":"+ai_site+":GAIN:ALL"
    caput(command_str,gain)
    


def set_TRG(trg_value):
    command_str = ao_uut+":"+ao_site+":TRG"
    caput(command_str,trg_value)

    
def getAmbTemp():
    command_str = ai_uut+":SYS:0:TEMP"
    amb_temp = caget(command_str)
    return amb_temp

def set_ACQ43X_sample_rate(rate):
    command_str = ai_uut+":1:ACQ43X_SAMPLE_RATE"
    caput(command_str,rate)

def start_stream():
    command_str = ai_uut+":MODE:CONTINUOUS"
    caput(command_str,1)

def stop_stream():
    command_str = ai_uut+":MODE:CONTINUOUS"
    caput(command_str,0)


############ Other useful incantations that may be built into functions ############

# caget('acq206_015:2:RANGE:01') for individual channel SPAN range
# caget('acq206_015:2:RANGE:ALL') for global SPAN setting
# 0 = UP5V
# 1 = UP10V
# 2 = 5V
# 3 = 10V



# Old way I tried to do completion poll
# This would have been elegant but I can't make it do what I want
#def wait_valldone(pvname=None, timestamp=None, value= None, **kw):
#    epics.camonitor_clear('KMUX:VALLDONE')
#    if value == 1:
#        print "Capture COMPLETE\n"
#        complete = 1
#        return complete
#
#wait_valldone('COMPLETE')
#while 1:
#    if complete == 1:
#        print "!!!!!!!!! Done !!!!!!!!!!!"
#        print complete
#        break
#    epics.camonitor('KMUX:VALLDONE')
#
#print "Exiting program"


