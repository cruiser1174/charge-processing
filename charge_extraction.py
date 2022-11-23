# -*- coding: utf-8 -*-
"""
Created on Sat Sep 18 17:38:06 2021

Author: Reuben Cruise - cruiser@tcd.ie
"""

import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np

#input file names

file_names = [ 
              'combined-pressure-data_1_30_12.7_2s_1_p_1.xlsx'
              ]

#t value dictionary for calculating t-test
t_vals = {1: 12.71,
          2: 4.403,
          3: 3.182,
          4: 2.776,
          5: 2.571,
          6: 2.447,
          7: 2.365,
          8: 2.306,
          9: 2.262,
          10: 2.228,
          11: 2.201,
          12: 2.179,
          13: 2.160,
          14: 2.145,
          15: 2.131,
          16: 2.12,
          17: 2.110,
          18: 2.101,
          19: 2.093,
          20: 2.086,
          21: 2.080,
          22: 2.074,
          23: 2.069,
          25: 2.064,
          26: 2.056,
          27: 2.052,
          28: 2.048,
          29: 2.045,
          30: 2.042}
# gets the section in a string after before the pos-th underscore
def get_quantity(string,pos):
    start_ind = 0
    end_ind = 0
    count = 1
    for i in range(len(string)):
        if(string[i]=='_'):
            if(count == pos):
                end_ind = i
                break
            else:
                count+=1
                if(count == pos):
                    start_ind = i+1
                    if(pos == 8):
                        end_ind = len(string)-5
                        break
    return string[start_ind:end_ind]

# Adds a column to df of the slope between each 2 datapoints, where the first 
# point is = 0
def append_slopes(df):
    slope_ts = []
    charge_ts = df.charge
    for i in range(df.shape[0]):
        if i == 0:
            slope_ts.append(0)
        else:
            slope_ts.append(charge_ts[i]-charge_ts[i-1])
    df['slope']=slope_ts

def get_charge_ts(df):
    return df.charge

def get_slopes(df):
    slope_ts = []
    charge_ts = get_charge_ts(df)
    for i in range(df.shape[0]):
        if i == 0:
            slope_ts.append(0)
        else:
            slope_ts.append(charge_ts[i]-charge_ts[i-1])
    return slope_ts

def get_charges(file_name):
    batch = get_batch(file_name)
    num = get_num(file_name)
    run = get_run(file_name)
    interval = get_interval_6(file_name)
    df = pd.read_excel(file_name)
    slope_ts = get_slopes(df)
    charges = []
    charges_x = []
    cond = False
    charge = 0
    charge_no = 1
    for i in range(df.shape[0]):
        slope = slope_ts[i]
        if slope <= -interval:
            charge += slope
            cond = True
        if slope > -interval:
            #print('num {} batch {} run {} charge no: {}'.format(num, batch, run, charge_no))
            if cond:
                if(charge<0):
                    
                    if(len(charges) > 0):
                        
                        if(charge < (charges[len(charges)-1]/1.2)):
                            charges.append(charge)
                            charges_x.append(charge_no)
                            cond = False
                            charge_no +=2
                    else:
                        charges.append(charge)
                        charges_x.append(charge_no)
                        cond = False
                        charge_no +=2
                charge = 0
    return [charges_x,charges]

def add_cpp(df):
    cpp_vals = []
    for i in range(df.shape[0]):
        cpps = []
        particle_no = float(df['Number of Particles'][i])
        charges = df['Charge'][i]
        for j in range(len(charges)):
            cpps.append(charges[j]/particle_no)
        cpp_vals.append(cpps)
    df['CPP'] = cpp_vals
    
def add_scd(df):
    scd_vals = []
    for i in range(df.shape[0]):
        scds = []
        particle_no = float(df['Number of Particles'][i])
        charges = df['Charge'][i]
        diam = float(df['Diameter'][i])
        for j in range(len(charges)):
            scds.append((charges[j]*1e+06)/(particle_no*math.pi*((diam*1e-03)**2)))
        scd_vals.append(scds)
    df['SCD'] = scd_vals

def get_interval_12(file_name):
    N = get_quantity(file_name, 6)
    return(float(N)*(2.5e-11))
    
def get_interval_6(file_name):
    N = get_quantity(file_name, 6)
    return(float(N)*(1.4e-12))

def get_interval_6(file_name):
    N = get_quantity(file_name, 6)
    return(float(N)*(1.4e-12))

def get_material(file_name):
    return(get_quantity(file_name, 1))

def get_humidity(file_name):
    return(float(get_quantity(file_name, 2)))

def get_temp(file_name):
    return(float(get_quantity(file_name, 3)))

def get_diam(file_name):
    return(float(get_quantity(file_name, 4)))

def get_delay(file_name):
    return(get_quantity(file_name, 5))

def get_num(file_name):
    return(int(get_quantity(file_name, 6)))

def get_batch(file_name):
    return('B{}'.format(get_quantity(file_name, 7)))

def get_run(file_name):
    print(file_name)
    return(int(file_name.split('_')[-1].split('.')[0]))

def get_confidence(df):
    new_df = df.iloc[:, :-1]
    N = new_df.shape[1]
    new_df['stdev'] = new_df.std(axis = 1, ddof = 0)
    new_df['ster'] = new_df['stdev']/np.sqrt(N)
    new_df['Confidence'] = t_vals[N]*new_df['ster']
    return new_df['Confidence']

def get_batch_data(data_file, diameter, number, batch, charge_type):
    df = pd.DataFrame()
    for i in range(data_file.shape[0]):
        num = data_file['Number of Particles'][i]
        bat = data_file['Batch'][i]
        diam = data_file['Diameter'][i]
        if num == number and bat == batch and diam == diameter:
            run = data_file['Run'][i]
            col_name = '{} x {} mm Batch {} Run {}'.format(number, diameter, batch, int(run))
            df[col_name] = data_file[charge_type][i]
    df['Average {} x {} mm Batch {}'.format(number, diameter, batch)] = df.mean(axis=1)
    df['{} Confidence'.format(batch)] = get_confidence(df)
    return df

def get_number_data(data_file, diameter, number, charge_type):
    output_df = pd.DataFrame()
    output_df['Contact']=data_file['Charge Number'][0]
    df_len = output_df.shape[0]
    for i in range(data_file.shape[0]):
        num = data_file['Number of Particles'][i]
        diam = data_file['Diameter'][i]
        if num == number and diam == diameter:
            run = data_file['Run'][i]
            batch = data_file['Batch'][i]
            col_name = '{} x {} mm Batch {} Run {}'.format(number, diameter, batch, int(run))
            col_data = data_file[charge_type][i]
            col_len = len(col_data)
            if col_len < df_len:
                dif = df_len - col_len
                counter = 0
                while counter < dif:
                    col_data.append(None)
                    counter+=1
            output_df[col_name] = col_data
    av_data = output_df.drop('Contact', axis = 1)
    output_df['Average {} x {} mm Batch {}'.format(number, diameter, batch)] = av_data.mean(axis=1)
    output_df['{} Confidence'.format(batch)] = get_confidence(av_data)
    return output_df

def make_data_file(file_name):
    df = pd.DataFrame()
    file_data = get_file_data(file_name)
    df = df.append(file_data, ignore_index = True)
    output = pd.DataFrame()
    add_cpp(df)
    add_scd(df)
    output['Contact'] = df['Charge Number'][0]
    output['Charge'] = df['CPP'][0]
    output['Surface Charge Density'] = df['SCD'][0]
    output.to_excel('{}_Charges.xlsx'.format(file_name[:len(file_name)-5]))

def get_file_data(file_name):
    data = {}
    data['Material']=get_material(file_name)
    data['Humidity']=get_humidity(file_name)
    data['Temperature']=get_temp(file_name)
    data['Diameter']=get_diam(file_name)
    data['Flip Delay']=get_delay(file_name)
    data['Number of Particles']=get_num(file_name)
    data['Batch']=get_batch(file_name)
    data['Run']=get_run(file_name)
    
    file_charge_data = get_charges(file_name)
    
    data['Charge Number']=file_charge_data[0]
    data['Charge']=file_charge_data[1]
    return data

def plot_col(data,col,title,y_label, y_lim):
    plt.figure()
    for i in range(data.shape[0]):
        plt.plot(charge_data['Charge Number'][i],
                 charge_data[col][i], 
                 label = '{}_{}_{}'.format(int(charge_data['Number of Particles'][i]), 
                                        charge_data['Batch'][i],
                                        int(charge_data['Run'][i])))
    plt.legend()
    plt.title(title)
    plt.xlabel('Contacts')
    plt.ylabel(y_label)
    #plt.ylim(-6,y_lim)
    #plt.xlim(0,150)
    

def save_data(data_file, size, data_column):
    output_df = pd.DataFrame()
    output_df['Contact']=data_file['Charge Number'][0]
    df_len = output_df.shape[0]
    print('DF length = {}'.format(df_len))
    for i in range(data_file.shape[0]):
        column_name = '{} x {} mm Batch {} Run {}'.format(int(data_file['Number of Particles'][i]),
                                                          data_file['Diameter'][i], 
                                                          data_file['Batch'][i], 
                                                          int(data_file['Run'][i]))
        col_data = data_file[data_column][i]
        col_len = len(col_data)
        print(column_name)
        print('len = {}'.format(len(col_data)))
        if col_len < df_len:
            dif = df_len - col_len
            counter = 0
            while counter < dif:
                col_data.append(None)
                counter+=1
                print('Col NaN added')
        
        print('len = {}'.format(len(col_data)))
        
        
        output_df[column_name] = col_data
    
    output_df.to_excel('combined_data_{}_{}.xlsx'.format(size, data_column))

nums = [1,2,4,8,16,32]
if __name__ == '__main__':
    charge_data = pd.DataFrame()
    for i in range(len(file_names)):
        file_name = file_names[i]
        #make_data_file(file_name)
        file_data = get_file_data(file_name)
        charge_data = charge_data.append(file_data, ignore_index = True)
    
    add_cpp(charge_data)
    add_scd(charge_data)
    
    """
    for num in nums:
        print('num = {}'.format(num))
        print('SCD')
        scd_data = get_number_data(charge_data, 12.7, num, 'SCD')
        scd_data.to_excel('PTFE_{}_12.7mm_SCD.xlsx'.format(num))
        print('CPP')
        cpp_data = get_number_data(charge_data, 12.7, num, 'CPP')
        cpp_data.to_excel('PTFE_{}_12.7mm_CPP.xlsx'.format(num))
        print('Charge')
        charges_data = get_number_data(charge_data, 12.7, num, 'Charge')
        charges_data.to_excel('PTFE_{}_12.7mm_Charge.xlsx'.format(num))
    """
    
    #save_data(charge_data, 6.35,  'Charge')
    save_data(charge_data, '6.35_256_roll_long_wait_1',  'CPP')
   # save_data(charge_data, 3.969, 'SCD')
    
    plot_col(charge_data, 
             'Charge', 
             'Total Charge', 
             'Charge (C)',
             -20E-09)
    
    plot_col(charge_data, 
             'CPP', 
             'Charge per Particle', 
             'Charge per Particle (C)',
             -1.25E-09)
    
    plot_col(charge_data, 
             'SCD', 
             'Surface Charge Density', 
             'Surface Charge Density (uC/m2)',
             -10)
    plt.show()
    
    
