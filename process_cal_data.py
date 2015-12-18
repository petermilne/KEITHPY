#!/usr/bin/python

import sys;import time;import csv;import scipy
import numpy as np
import epics;from epics import caget, caput
import keith_func
import global_uut_settings
import matplotlib.pyplot as plt
import subprocess
import os
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.etree.ElementTree import Element, SubElement, Comment
from xml.dom import minidom

ai_uut = global_uut_settings.ai_uut
ao_uut = global_uut_settings.ao_uut
ai_site = global_uut_settings.ai_site
ao_site = global_uut_settings.ao_site

def process(date_time,model,nchan,serial_num,temperature,samp_rate,firm_rev,fpga_rev):
    
    if 'ACQ435' in model:
        # Add in 437 option. Which will be mix of operating speeds and gains :/
        filename = serial_num+"_hires"
        ch_data = np.array([callOctave(filename,nchan)]); # Create array from ch_data
        
        filename = serial_num+"_hispeed"
        ch_data = np.vstack((ch_data,[callOctave(filename,nchan)])); # Append vertically to extend array
        
    elif 'ACQ437' in model :
        filename = serial_num+"_hires_gain0"
        ch_data = np.array([callOctave(filename,nchan)])
        
        filename = serial_num+"_hires_gain1"
        ch_data = np.vstack((ch_data,[callOctave(filename,nchan)]))
        filename = serial_num+"_hires_gain2"
        ch_data = np.vstack((ch_data,[callOctave(filename,nchan)]))
        filename = serial_num+"_hires_gain3"
        ch_data = np.vstack((ch_data,[callOctave(filename,nchan)]))
        filename = serial_num+"_hispeed_gain0"
        ch_data = np.vstack((ch_data,[callOctave(filename,nchan)]))
        filename = serial_num+"_hispeed_gain1"
        ch_data = np.vstack((ch_data,[callOctave(filename,nchan)]))
        filename = serial_num+"_hispeed_gain2"
        ch_data = np.vstack((ch_data,[callOctave(filename,nchan)]))
        filename = serial_num+"_hispeed_gain3"
        ch_data = np.vstack((ch_data,[callOctave(filename,nchan)]))
    elif 'ACQ420' in model or 'ACQ425' in model :
        filename = serial_num+"_gain0"
        ch_data = np.array([callOctave(filename,nchan)])
        
        filename = serial_num+"_gain1"
        ch_data = np.vstack((ch_data,[callOctave(filename,nchan)]))
        filename = serial_num+"_gain2"
        ch_data = np.vstack((ch_data,[callOctave(filename,nchan)]))
        filename = serial_num+"_gain3"
        ch_data = np.vstack((ch_data,[callOctave(filename,nchan)]))
    elif 'ACQ42' in model :
        filename = serial_num
        ch_data = np.array([callOctave(filename,nchan)])
    
    ################################################ Begin XML Generation
    
    # Standard Header
    top = Element('ACQ')
    acqcal = SubElement(top, 'AcqCalibration')
    
    info = SubElement(acqcal, 'Info')
    info_1 = SubElement(info, 'CalDate')
    info_1.text = str(date_time)
    info_2 = SubElement(info, 'Carrier')
    info_2.text = str(ai_uut)
    info_3 = SubElement(info, 'Model')
    info_3.text = str(model)
    info_4 = SubElement(info, 'SerialNum')
    info_4.text = str(serial_num)
    info_5 = SubElement(info, 'Temperature')
    info_5.text = str(temperature)
    info_6 = SubElement(info, 'SampleRate')
    info_6.text = str(samp_rate)
    info_7 = SubElement(info, 'FirmwareRev')
    info_7.text = str(firm_rev)
    info_8 = SubElement(info, 'FPGAInfo')
    info_8.text = str(fpga_rev)
    
    ############################################ Calibration Data Insertion
    max_codes, min_codes, res = queryWordLength(model)
        
    #data = SubElement(acqcal, 'Data', AICHAN=str(nchan), code_min=str(min_codes), code_max=str(max_codes))
    
    if 'ACQ437' in model :
        data = SubElement(acqcal, 'Data', AICHAN=str(nchan), code_min=str(min_codes), code_max=str(max_codes), SW="hi_res_mode,gain%d")
        # ACQ437 - Combine ranges and adc speed modes - SPECIAL CASE
        hires_g0 = SubElement(data, 'Range', name="HI_RES_10V", sw="1,0")
        hires_g1 = SubElement(data, 'Range', name="HI_RES_5V", sw="1,1")
        hires_g2 = SubElement(data, 'Range', name="HI_RES_2V", sw="1,2")
        hires_g3 = SubElement(data, 'Range', name="HI_RES_1V", sw="1,3")
        hispeed_g0 = SubElement(data, 'Range', name="HI_SPEED_10V", sw="0,0")
        hispeed_g1 = SubElement(data, 'Range', name="HI_SPEED_5V", sw="0,1")
        hispeed_g2 = SubElement(data, 'Range', name="HI_SPEED_2V", sw="0,2")
        hispeed_g3 = SubElement(data, 'Range', name="HI_SPEED_1V", sw="0,3")
        SubElement(hires_g0, 'Nominal', roff="0", eslo=str(20.0/np.power(2,res)), eoff="0")
        SubElement(hires_g1, 'Nominal', roff="0", eslo=str(10.0/np.power(2,res)), eoff="0")
        SubElement(hires_g2, 'Nominal', roff="0", eslo=str(4.0/np.power(2,res)), eoff="0")
        SubElement(hires_g3, 'Nominal', roff="0", eslo=str(2.0/np.power(2,res)), eoff="0")
        SubElement(hispeed_g0, 'Nominal', roff="0", eslo=str(20.0/np.power(2,res)), eoff="0")
        SubElement(hispeed_g1, 'Nominal', roff="0", eslo=str(10.0/np.power(2,res)), eoff="0")
        SubElement(hispeed_g2, 'Nominal', roff="0", eslo=str(4.0/np.power(2,res)), eoff="0")
        SubElement(hispeed_g3, 'Nominal', roff="0", eslo=str(2.0/np.power(2,res)), eoff="0")
        for i in range(1,nchan+1) :
            split_params = ch_data[0][i-1]
            SubElement(hires_g0, 'Calibrated', ch=str(i), eslo=str(split_params[0]), eoff=str(split_params[1]))
            split_params = ch_data[1][i-1]
            SubElement(hires_g1, 'Calibrated', ch=str(i), eslo=str(split_params[0]), eoff=str(split_params[1]))
            split_params = ch_data[2][i-1]
            SubElement(hires_g2, 'Calibrated', ch=str(i), eslo=str(split_params[0]), eoff=str(split_params[1]))
            split_params = ch_data[3][i-1]
            SubElement(hires_g3, 'Calibrated', ch=str(i), eslo=str(split_params[0]), eoff=str(split_params[1]))
            split_params = ch_data[4][i-1]
            SubElement(hispeed_g0, 'Calibrated', ch=str(i), eslo=str(split_params[0]), eoff=str(split_params[1]))
            split_params = ch_data[5][i-1]
            SubElement(hispeed_g1, 'Calibrated', ch=str(i), eslo=str(split_params[0]), eoff=str(split_params[1]))
            split_params = ch_data[6][i-1]
            SubElement(hispeed_g2, 'Calibrated', ch=str(i), eslo=str(split_params[0]), eoff=str(split_params[1]))
            split_params = ch_data[7][i-1]
            SubElement(hispeed_g3, 'Calibrated', ch=str(i), eslo=str(split_params[0]), eoff=str(split_params[1]))
        
    elif 'ACQ43' in model :
        data = SubElement(acqcal, 'Data', AICHAN=str(nchan), code_min=str(min_codes), code_max=str(max_codes), SW="hi_res_mode,gain%d")
        # ACQ43X
        hires_g0 = SubElement(data, 'Range', name="HI_RES_10V", sw="1,0")
        hispeed_g0 = SubElement(data, 'Range', name="HI_SPEED_10V", sw="0,0")
        SubElement(hires_g0, 'Nominal', roff="0", eslo=str(20.0/np.power(2,res)), eoff="0")
        SubElement(hispeed_g0, 'Nominal', roff="0", eslo=str(20.0/np.power(2,res)), eoff="0")
        for i in range(1,nchan+1) :
            split_params = ch_data[0][i-1]
            SubElement(hires_g0, 'Calibrated', ch=str(i), eslo=str(split_params[0]), eoff=str(split_params[1]))
            split_params = ch_data[1][i-1]
            SubElement(hispeed_g0, 'Calibrated', ch=str(i), eslo=str(split_params[0]), eoff=str(split_params[1]))

    elif 'ACQ420' in model or 'ACQ425' in model :
        data = SubElement(acqcal, 'Data', AICHAN=str(nchan), code_min=str(min_codes), code_max=str(max_codes), SW="gain%d")
        # ACQ42X GAINS
        gain0 = SubElement(data, 'Range', name="10V", sw="0")
        gain1 = SubElement(data, 'Range', name="5V", sw="1")
        gain2 = SubElement(data, 'Range', name="2.5V", sw="2")
        gain3 = SubElement(data, 'Range', name="1.25V", sw="3")
        SubElement(gain0, 'Nominal', roff="0", eslo=str(20.0/np.power(2,res)), eoff="0")
        SubElement(gain1, 'Nominal', roff="0", eslo=str(20.0/np.power(2,res)), eoff="0")
        SubElement(gain2, 'Nominal', roff="0", eslo=str(20.0/np.power(2,res)), eoff="0")
        SubElement(gain3, 'Nominal', roff="0", eslo=str(20.0/np.power(2,res)), eoff="0")
        for i in range(1,nchan+1):
            split_params = ch_data[0][i-1]
            SubElement(gain0, 'Calibrated', ch=str(i), eslo=str(split_params[0]), eoff=str(split_params[1]))
            split_params = ch_data[1][i-1]
            SubElement(gain1, 'Calibrated', ch=str(i), eslo=str(split_params[0]), eoff=str(split_params[1]))
            split_params = ch_data[2][i-1]
            SubElement(gain2, 'Calibrated', ch=str(i), eslo=str(split_params[0]), eoff=str(split_params[1]))
            split_params = ch_data[3][i-1]
            SubElement(gain3, 'Calibrated', ch=str(i), eslo=str(split_params[0]), eoff=str(split_params[1]))
            
    elif 'ACQ42' in model :
       data = SubElement(acqcal, 'Data', AICHAN=str(nchan), code_min=str(min_codes), code_max=str(max_codes))
       # ACQ42X NO GAINS
       gain0 = SubElement(data, 'Range', name="10V")
       SubElement(gain0, 'Nominal', roff="0", eslo=str(20.0/np.power(2,res)), eoff="0")
       for i in range(1,nchan+1):
            split_params = ch_data[0][i-1]
            SubElement(gain0, 'Calibrated', ch=str(i), eslo=str(split_params[0]), eoff=str(split_params[1]))
            
    
    # Standerd Footer
    model_spec = SubElement(top, 'ModelSpec')
    bwidth, bset = getBanks(model,nchan)
    ch_block = SubElement(model_spec, 'ChannelBlockMask')
    block_width = SubElement(ch_block, 'BlockWidth')
    block_width.text = str(bwidth)
    block_set = SubElement(ch_block, 'BlockSet')
    block_set.text = bset
    max_rate = SubElement(ch_block, 'MaxDeviceRate')
    rate = getRate(fpga_rev)
    max_rate.text = rate+" S/sec"
    
    # Print XML to console and file
    print prettify(top)
    fid = open('./cal_files/'+serial_num+'.xml', 'w')
    fid.write(prettify(top))
    fid.closed

    # Cleanup txt files
    command = "rm ./cal_files/*.txt"
    os.system(command)





def callOctave(filename,nchan):
    str_nchan = str(nchan)
    command='octave --silent --eval \"adc_linearity_test(\''+filename+'\','+str_nchan+')\"'
    print command
    # Run commands
    cwd = os.getcwd()      # Return the current working directory
    os.chdir('/home/projects/ACQ400/KeithPy/octave')   # Change current working directory
    os.system(command)
    os.chdir(cwd)   # Return to original working directory
    
    command = "evince \"/home/projects/ACQ400/KeithPy/octave/adc_linearity_results/"+filename+"_Linearity_Test.pdf\""
    os.system(command)
    raw_input('\033[1m'+"Survey linearity graph and press Enter to continue..."+'\033[0m')
    
    # Pull data from .txt file
    ch_data = np.loadtxt('./cal_files/'+filename+'.txt',skiprows=1,usecols=(2,3))
    return ch_data
    

def queryWordLength(model) :
    if 'ACQ42' in model:
        res = 16
    elif 'ACQ43' in model :
        res = 24
    else :
        print "Card resolution not found"
        exit()
    
    max_codes = np.power(2,res-1) - 1
    min_codes = -np.power(2,res-1)
    return (max_codes, min_codes, res)
    

def getBanks(model, nchan):
    if 'ACQ435' in model :
        bwidth = 8
        bset = "1111,1110,1100,1000,0100,0010,0001"
    elif 'ACQ437' in model :
        bwidth = 8
        bset = "11,10,01"
    else :
        bwidth = nchan
        bset = "1"

    return (bwidth, bset)


def getRate(fpga):
    if 'A1' in fpga or 'A5' in fpga :
        rate = str(2000000)
    elif '_01' in fpga or '05' in fpga or '04' in fpga :
        rate = str(1000000)
    elif '08' in fpga :
        rate = str(50000000)
    else :
        rate = str(128000)

    return rate


def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")
    