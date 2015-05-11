#!/usr/bin/python

import sys;import time;import csv;import scipy
import numpy as np
import epics;from epics import caget, caput
import keith_func
import global_uut_settings
import matplotlib.pyplot as plt

uut = global_uut_settings.uut
ai_site = global_uut_settings.ai_site
ao_site = global_uut_settings.ao_site

print sys.argv[0]
channel = sys.argv[1]
print "CC"+channel

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


print (keith_func.get435code(channel))
        
