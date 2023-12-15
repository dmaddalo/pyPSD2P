import numpy as np
import os
import pandas as pd
import linecache
import h5py

def f(directory):
    # files = glob.glob(os.path.join(directory,'*.txt'))
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            # with open(os.path.join(directory,filename),'r') as file:
                # alldata = [line.strip() for line in file.readlines()]
            tempdata = pd.read_csv(os.path.join(directory,filename), \
                                   sep='\t',header=23,dtype=float)
            tempdata = np.array(tempdata.dropna(axis=1))
            # trial = np.array(alldata[24:-1])
            if not 'WaveData' in locals():
                WaveData = tempdata[...,np.newaxis]
            else:
                WaveData = np.dstack((WaveData,tempdata))

    if 'WaveData' in locals():
        tlim = linecache.getline(os.path.join(directory,filename),7).strip()
        tlim = float(tlim[21:32])
    else:
        raise TypeError('No dataset found in ' + directory + 
                        '.\nWaveData does not exist. Check directory again.')

    t = np.linspace(0,tlim,WaveData.shape[0])

    return WaveData,t

#%% For HETs simulation dataset. Called by 'mainsim.py'

def fsim(directory):
    
    with h5py.File(directory + os.sep + 'PostData_SPT100_HET_big.hdf5','r') as tempdata:
        WaveData = tempdata['picM_data']['n'][()]
        t = tempdata['times_sim'][()]
            
    with h5py.File(directory + os.sep + 'SimState_SPT100_HET.hdf5','r') as tempdata:
        z = tempdata['picM']['zs'][()]
        r = tempdata['picM']['rs'][()]
       
    return WaveData,t,z,r

#%% For camera dataset (Victor). Called by 'maincam.py'

def fcam(directory):
    
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            tempdata = pd.read_csv(os.path.join(directory,filename), \
                                   sep=',',header=None,dtype=float)
                
            if not 'WaveData' in locals():
                WaveData = np.array(tempdata)[:,1:-1,np.newaxis]
                t = np.array(tempdata)[:,0]
            else:
                WaveData = np.dstack((WaveData,tempdata))
                
    if WaveData.shape[2] == 1:
        WaveData = WaveData[:,:,0]
            
    return WaveData,t
    