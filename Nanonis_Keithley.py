from nanonis_control import nanonis_tcp
nanonis = nanonis_tcp.nanonis_programming_interface(IP = '127.0.0.1', PORT = 6501)

from pymeasure.instruments.keithley import Keithley2400
from pymeasure.adapters import VISAAdapter
import time
import tkinter as tk
from tkinter import *
import os
import numpy as np
import matplotlib.pyplot as plt



adapter = VISAAdapter("ASRL7::INSTR",  read_termination='\r', timeout=5000)
keithley = Keithley2400(adapter)
# keithley.shutdown()

keithley.apply_voltage()
keithley.source_voltage_range = 1
keithley.compliance_current = 5e-3
source_voltage_start = 0 # mV
source_voltage_steps = 101
source_voltage_end = 0 # mV
source_voltage_interval = (source_voltage_end-source_voltage_start)/(source_voltage_steps - 1)

V_bias_start = 3.7 # V
V_bias_steps = source_voltage_steps
V_bias_end = 3.3 # V
V_bias_interval = (V_bias_end - V_bias_start)/(V_bias_steps - 1)

for i in range(source_voltage_steps):
    
    keithley.enable_source()
    time.sleep(0.2)
    keithley.measure_current()
    keithley.source_voltage = 1e-3*(source_voltage_start + source_voltage_interval*i)
    print('current =', 1e3*keithley.current, 'mA')
    time.sleep(0.5)
    nanonis.send('Bias.Set', 'float32', V_bias_start + V_bias_interval*i)
    if i%2 == 0:
        nanonis.ScanAction('start', 'down')
        nanonis.ScanWaitEndOfScan()
    else:
        nanonis.ScanAction('start', 'up')
        nanonis.ScanWaitEndOfScan()
    

# keithley.shutdown()
    