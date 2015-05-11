#!/usr/bin/python

import sys;import time;import csv;import scipy
import numpy as np
import epics;from epics import caget, caput
import keith_func
import global_uut_settings
import matplotlib.pyplot as plt


print sys.argv[0]
voltage = sys.argv[1]
print voltage

nchan = 32

############ Begin setting AO voltages and reading back from Keithley #########
''' Serves as block comment
keith_func.set_AO_all(5,4)
Vall = keith_func.getKVolts_all(32)
print Vall

keith_func.set_AO_all(3,4)
Vall = keith_func.getKVolts_all(32)
print Vall
'''

keith_func.set_TRG(0)
keith_func.set_SPAN_all(3)

time.sleep(1)

keith_func.set_AO_all(voltage,nchan)   # Set AO on current channel
