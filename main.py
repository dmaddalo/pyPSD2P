#%% IMPORT
# from general import *
from ioload import chunking, definefolder, wfm2mat
from visual import separateplots
from iopsd2p import binpsd2p, computefft,computestats, csd
import matplotlib.pyplot as plt
import numpy as np
import os

class structured:
    def __getattr__(self,name):
        self.__dict__[name] = structured()
        return self.__dict__[name]

#%% DEFINITIONS

## d = axial distance [mm]
d = 20
## alpha = angular displacement [deg]
alpha = 50
## SCCM
mdot = 1.4
##
rot = 25
forced = 0
day = '16.10'
## Number of chunks in which to divide the waveform
chunks = 1
## Binning parameters (none of those depend on the dataset)
df = 200       # Hz
dk = 3         # deg
flim = 1e5     # upper limit frequency

#%% INPUT-OUTPUT

directory = definefolder.f(mdot,d,alpha,day)

if forced:
    directory = directory+"-forced"

WaveData, t = wfm2mat.f(directory)

WaveData_c, t_c = chunking.f(t,WaveData,chunks)

params = {'mdot':mdot,'d':d,'alpha':alpha}

#%% PERFORM FFTs
# WaveData_t = np.zeros((WaveData_c.shape),dtype=np.complex_)
temp = []
for i in range(0,WaveData_c.shape[2]):
    # fRFT, WaveData_t = computefft.f(t_c,WaveData_c[:,:,i])
    temp.append(computefft.f(t_c,WaveData_c[:,:,i]))

    if i == 0:
        WaveData_t = temp[i][1]
        fRFT = temp[i][0]
    else:
        WaveData_t = np.dstack((WaveData_t,temp[i][1]))

del temp


if df < fRFT[1]-fRFT[0]:
    df = fRFT[1]-fRFT[0]

fRFTbin = np.arange(fRFT[0],flim+df,df)

#%% COMPUTE SPECTRAL DENSITIES
csd32,psd3,psd2,fRFTcut = csd.f(WaveData_t[:,2,:],WaveData_t[:,1,:],fRFT,flim,chunks)

csd24,_,psd4,_ = csd.f(WaveData_t[:,1,:],WaveData_t[:,3,:],fRFT,flim,chunks)

csd12,psd1,_,_ = csd.f(WaveData_t[:,0,:],WaveData_t[:,1,:],fRFT,flim,chunks)

#%% CORRECT PROBE ORIENTATION
# Provisional, only accounts for counterclockwise rotation along the
# azimuthal direction

csdaz = {'pow':abs(csd32),'ang':np.angle(csd32),'orig':csd32}

csdax = {}
csdax['pow'] = np.sqrt(abs(csd24)**2*np.cos(np.deg2rad(rot))**2 +
                          abs(csd12)**2*np.sin(np.deg2rad(rot))**2)
csdax['ang'] = np.angle(csd24)*np.cos(np.deg2rad(rot)) - \
                    np.angle(csd12)*np.sin(np.deg2rad(rot))
csdax['orig'] = csd24
      
csdrd = {}
csdrd['pow'] = np.sqrt(abs(csd24)**2*np.sin(np.deg2rad(rot))**2 +
                          abs(csd12)**2*np.cos(np.deg2rad(rot))**2)
csdrd['ang'] = np.angle(csd24)*np.sin(np.deg2rad(rot)) + \
                    np.angle(csd12)*np.cos(np.deg2rad(rot))
csdrd['orig'] = csd12

#%% COMPUTE PSD2Ps

kkaz,ffaz,hhaz = binpsd2p.f(fRFT,csdaz['ang'],csdaz['pow'],fRFTbin,
                        np.arange(-np.pi,np.pi,np.deg2rad(dk)))

kkax,ffax,hhax = binpsd2p.f(fRFT,csdax['ang'],csdax['pow'],fRFTbin,
                        np.arange(-np.pi,np.pi,np.deg2rad(dk)))

kkrd,ffrd,hhrd = binpsd2p.f(fRFT,csdrd['ang'],csdrd['pow'],fRFTbin,
                        np.arange(-np.pi,np.pi,np.deg2rad(dk)))

#%% COMPUTE STATISTICS

statsaz = computestats.f(csdaz,psd3,psd2,fRFT,df,flim)

statsax = computestats.f(csdax,psd2,psd4,fRFT,df,flim)

statsrd = computestats.f(csdrd,psd1,psd2,fRFT,df,flim)

## ROTATE COHERENCE

mscaz = abs(statsaz['coherence']**2)
mscax = abs(statsax['coherence']**2*np.cos(np.deg2rad(rot))**2 + 
            abs(statsrd['coherence']**2*np.sin(np.deg2rad(rot))**2))
mscrd = abs(statsax['coherence']**2*np.sin(np.deg2rad(rot))**2 + 
            abs(statsrd['coherence']**2*np.cos(np.deg2rad(rot))**2))

statsaz['coherence'] = mscaz
statsax['coherence'] = mscax
statsrd['coherence'] = mscrd

#%% PLOT

kk = {'az':kkaz,'ax':kkax,'rd':kkrd}
ff = {'az':ffaz,'ax':ffax,'rd':ffrd}
hh = {'az':hhaz,'ax':hhax,'rd':hhrd}
stats = {'az':statsaz,'ax':statsax,'rd':statsrd}

separateplots.f(kk,ff,hh,stats,params)

    
# cdict = {
#   'red'  :  ( (0.0, 0.25, .25), (0.02, .59, .59), (1., 1., 1.)),
#   'green':  ( (0.0, 0.0, 0.0), (0.02, .45, .45), (1., .97, .97)),
#   'blue' :  ( (0.0, 1.0, 1.0), (0.02, .75, .75), (1., 0.45, 0.45))
# }
# cm = m.colors.LinearSegmentedColormap('mycmap',cdict,1024)
# plt.figure()
# plt.pcolor(kk,ff,hh,cmap=cm,vmin=1e-11,vmax=1e-4)
# plt.colorbar()








