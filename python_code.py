# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 14:23:53 2020

Author: Reuben Cruise - cruiser@tcd.ie
"""
import pandas as pd
import pyvisa
import time
import os
import numpy as np
import math
 
rm = pyvisa.ResourceManager()
name = rm.list_resources()
print(name)
K6517B = rm.get_instrument('ASRL4::INSTR')

K6517B.timeout = None
K6517B.chunk_size = 102400
K6517B.read_termination = '\n'
materials = ['PVC',
             'PTFE',
             'ALO',
             'LDPE',
             'HDPE']
particles = {'1/16': 1.5875,
             '0.086':2.185,
             '7/66':2.694,
             '1/8':3.175,
             '5/32':3.969,
             '3/16':4.7625,
             '7/32':5.55625,
             '1/4':6.35,
             '9/32':7.14375,
             '5/16':7.9375,
             '3/8':9.525,
             '13/32':10.3187,
             '7/16':11.1125,
             '1/2':12.7,
              '9/16':14.2875,
             '5/8':15.875,
             '7/8':22.225}

diam = '6.35'
P = '4.5e-4'
delay = '2s'
num = '64'
batch = '1'
run = '2'
mat = 'PTFE'

readings = open('{}_{}_30_{}_{}_{}_{}_{}.txt'.format(mat, P, diam, delay, num,batch,run), "w")
                                                            

data = K6517B.query(':TRAC:DATA?\n')

lbdata = data.replace(",000extchan,","\n")
coulsep = lbdata.replace("COUL",",C")
secsep = coulsep.replace("secs",",s")
nochan = secsep.replace("RDNG#","")

readings.write(nochan)

readings.close()

def check_initial_charge(charge_str):
    cond = False
    if charge_str[len(charge_str)-1] == 'R':
        charge = float(charge_str.replace('R',''))
        if charge == 0:
            cond = True
    return cond

file_name = '{}_{}_30_{}_{}_{}_{}_{}.txt'.format(mat, P, diam, delay, num,batch,run)

with open(file_name, "r") as filestream:
    ln = 0
    i = 1
    for line in filestream:
        ln = line
        
        items = line.split(',')
        charges = []
        start_adding = False
        for i in range(int(len(items)/5)):
            
            charge_index = i*5
            
            if check_initial_charge(items[charge_index]):
                start_adding = True
            if start_adding:
                charges.append(float(items[charge_index].replace('R','').replace('N','').replace('O','')))

        df = pd.DataFrame(charges, columns = ['charge'])
        df.to_excel('{}_{}_30_{}_{}_{}_{}_{}.xlsx'.format(mat, P, diam, delay, num,batch,run))



