#!/usr/bin/python

import sys;import time;import csv;import scipy
import epics;from epics import caget, caput
import keith_func
import global_uut_settings


print sys.argv[0]
voltage = sys.argv[1]
print voltage

nchan = 32

keith_func.set_AO_all(voltage)   # Set AO on current channel
