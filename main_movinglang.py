#%% IMPORT
# from general import *
from ioload import chunking, definefolder, wfm2mat
from visual import separateplots
from iopsd2p import binpsd2p, computefft,computestats, csd
import matplotlib.pyplot as plt
import numpy as np

class structured:
    def __getattr__(self,name):
        self.__dict__[name] = structured()
        return self.__dict__[name]

#%% DEFINITIONS

## Langmuir probes (LPs) moving or fixed in space, 'fixedlang' or 'movinglang'. 
## This script mostly only supports the 'movinglang' option adequately. Use 
## 'main.py' for datasets in which the LPs are fixed.
lang = 'movinglang'     # do not change

## The positions below are referred to the LPs.
## When the LPs are fixed in space, the positions 'rho' and 'alpha' are to be
## intended the ones of the CP. Alternatively, if the LPs are moving in space,
## the aforementioned positions are referred to the LPs.
# rho = axial distance [mm]
rho = 70
# alpha = angular displacement [deg]
alpha = 0
# SCCM
mdot = 1.4
# Rotation to adjust the probes orientation. Only rotation along axis 1 is supported.
rot = 0
# Forced oscillations induced by the microwave generator, 1 (True) or 0 (False)
forced = 0
# Day of the acquisitions
day = '7.12'
# Any additional option (this is a parent folder of the main "mdot_rho_alpha"
# folder). Leave blank, i.e. '', if no additional option is to be specified.
opsparent = 'angularscan'
# Any additional option (this is a child folder of the main "mdot_rho_alpha"
# folder). Leave blank, i.e. '', if no additional option is to be specified.
opschild = ''
# Number of chunks in which to divide the waveform (equivalent to setting larger df)
chunks = 1
# Binning parameters (none of those depend on the dataset)
df = 200       # Hz
dk = 1         # deg
flim = 2e5     # upper limit frequency
cscale = 'log'      # colorscale for the dispersion plot, "log" or "lin"
savefig = False     # choose whether to save the output figures

#%% INPUT-OUTPUT

directory = definefolder.f(mdot,rho,alpha,lang,day,opsparent,opschild)

if forced:
    directory = directory+"-forced"

WaveData, t = wfm2mat.f(directory)

WaveData_c, t_c = chunking.f(t,WaveData,chunks)


params = {'mdot':mdot,'rho':rho,'alpha':alpha,'flim':flim,'colorscale':cscale}

if savefig == True:
    print('\nWarning: save figure option is set to true.')
    plt.close('all')

#%% PERFORM FFTs
# WaveData_t = np.zeros((WaveData_c.shape),dtype=np.complex_)

WaveData_m = np.mean(WaveData_c,axis=0)
WaveData_f = WaveData_c - WaveData_m

for i in range(0,WaveData_f.shape[2]):
    if i == 0:
        fRFT, WaveData_t = computefft.f(t,WaveData_f[:,:,i])
    else:
        WaveData_t = np.dstack((WaveData_t,computefft.f(t,WaveData_f[:,:,i],
                                                        returnf=False)))
        
#     # fRFT, WaveData_t = computefft.f(t_c,WaveData_c[:,:,i])
#     temp.append(computefft.f(t_c,WaveData_f[:,:,i]))

#     if i == 0:
#         WaveData_t = temp[i][1]
#         fRFT = temp[i][0]
#     else:
#         WaveData_t = np.dstack((WaveData_t,temp[i][1]))

# del temp


if df < fRFT[1]-fRFT[0]:
    df = fRFT[1]-fRFT[0]

fRFTbin = np.arange(fRFT[0],flim+df,df)

#%% COMPUTE SPECTRAL DENSITIES

if WaveData_t.ndim == 2:
    WaveData_t = WaveData_t[...,np.newaxis]

csd12,psd2,psd1,_ = csd.f(WaveData_t[:,1,:],WaveData_t[:,0,:],fRFT)

csd13,psd3,_,_ = csd.f(WaveData_t[:,2,:],WaveData_t[:,0,:],fRFT)

csd14,psd4,_,_ = csd.f(WaveData_t[:,3,:],WaveData_t[:,0,:],fRFT)

#%% CORRECT PROBE ORIENTATION
# Provisional, only accounts for counterclockwise rotation along the
# azimuthal direction

csdaz = {'pow':abs(csd12),'ang':np.angle(csd12),'orig':csd12}

csdax = {'pow':abs(csd13),'ang':np.angle(csd13),'orig':csd13}
      
csdrd = {'pow':abs(csd14),'ang':np.angle(csd14),'orig':csd14}
# csdrd = {'pow':abs(csd13),'ang':np.angle(csd13),'orig':csd13}

#%% COMPUTE STATISTICS

statsaz = computestats.f(csdaz,psd1,psd2,fRFT,df,flim)

statsax = computestats.f(csdax,psd1,psd3,fRFT,df,flim)

statsrd = computestats.f(csdrd,psd1,psd4,fRFT,df,flim)
# statsrd = computestats.f(csdrd,psd1,psd3,fRFT,df,flim)

## ROTATE COHERENCE

mscaz = abs(statsaz['coherence']**2)
mscax = abs(statsax['coherence']**2)
mscrd = abs(statsrd['coherence']**2)

statsaz['coherence'] = mscaz
statsax['coherence'] = mscax
statsrd['coherence'] = mscrd

#%% COMPUTE PSD2Ps, log scale with cross-power

if params['colorscale'] == 'log':
    kkaz,ffaz,hhaz = binpsd2p.f(fRFT,csdaz['ang'],csdaz['pow'],fRFTbin,
                            np.arange(-np.pi,np.pi,np.deg2rad(dk)))
    
    kkax,ffax,hhax = binpsd2p.f(fRFT,csdax['ang'],csdax['pow'],fRFTbin,
                            np.arange(-np.pi,np.pi,np.deg2rad(dk)))
    
    kkrd,ffrd,hhrd = binpsd2p.f(fRFT,csdrd['ang'],csdrd['pow'],fRFTbin,
                            np.arange(-np.pi,np.pi,np.deg2rad(dk)))

#%% COHERENCE PSD2Ps, linear scale with coherence

elif params['colorscale'] == 'lin':
    kkaz,ffaz,hhaz = binpsd2p.f(statsaz['fRFTbin'],statsaz['meanphase'],
                                statsaz['coherence'],fRFTbin,
                                np.arange(-np.pi,np.pi,np.deg2rad(dk)))
    
    kkax,ffax,hhax = binpsd2p.f(statsax['fRFTbin'],statsax['meanphase'],
                                statsax['coherence'],fRFTbin,
                                np.arange(-np.pi,np.pi,np.deg2rad(dk)))
    
    kkrd,ffrd,hhrd = binpsd2p.f(statsrd['fRFTbin'],statsrd['meanphase'],
                                statsrd['coherence'],fRFTbin,
                                np.arange(-np.pi,np.pi,np.deg2rad(dk)))

#%% PLOT

kk = {'az':kkaz, \
      'ax':kkax, \
      'rd':kkrd}
ff = {'az':ffaz, \
      'ax':ffax, \
      'rd':ffrd}
hh = {'az':hhaz, \
      'ax':hhax, \
      'rd':hhrd}
    
stats = {'az':statsaz, \
         'ax':statsax, \
         'rd':statsrd}

separateplots.f(kk,ff,hh,stats,params)

if savefig == True:
    from general import os
    
    figname = list()
    figname.append('azimuthal dispersion')
    figname.append('azimuthal cross power')
    figname.append('axial dispersion')
    figname.append('axial cross power')
    figname.append('radial dispersion')
    figname.append('radial cross power')
    figname.append('coherence')
    for i in range(plt.gcf().number):
        plt.figure(i+1)
        plt.savefig(str(directory + os.sep + figname[i] + '.png'))

    
# cdict = {
#   'red'  :  ( (0.0, 0.25, .25), (0.02, .59, .59), (1., 1., 1.)),
#   'green':  ( (0.0, 0.0, 0.0), (0.02, .45, .45), (1., .97, .97)),
#   'blue' :  ( (0.0, 1.0, 1.0), (0.02, .75, .75), (1., 0.45, 0.45))
# }
# cm = m.colors.LinearSegmentedColormap('mycmap',cdict,1024)
# plt.figure()
# plt.pcolor(kk,ff,hh,cmap=cm,vmin=1e-11,vmax=1e-4)
# plt.colorbar()








