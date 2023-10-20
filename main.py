# %%
from general import *
from inout import *
from ko import *
import matplotlib.pyplot as plt

# %%
## DEFINE

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
chunks = 10
## Binning parameters (none of those depend on the dataset)
df = 200       # Hz
dk = 3         # deg
flim = 1e5     # upper limit frequency

# %%
## INPUT OUTPUT

directory = definefolder.f(mdot,d,alpha,day)

if forced:
    directory = directory+"-forced"

WaveData, t = wfm2mat.f(directory)

WaveData_c, t_c = chunking.f(t,WaveData,chunks)

# %%
## PERFORM FFTs
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

# %%
## COMPUTE SPECTRAL DENSITIES
temp = CSD.f(WaveData_t[:,2,:],WaveData_t[:,1,:],fRFT,flim,chunks)
csd32 = temp[0]
psd3 = temp[1]
psd2 = temp[2]
fRFTcut = temp[3]

temp = CSD.f(WaveData_t[:,1,:],WaveData_t[:,3,:],fRFT,flim,chunks)
csd24 = temp[0]
psd4 = temp[2]

temp = CSD.f(WaveData_t[:,0,:],WaveData_t[:,1,:],fRFT,flim,chunks)
csd12 = temp[0]
psd1 = temp[1]

del temp

#%%
# CORRECT PROBE ORIENTATION
# Provisional, only accounts for counterclockwise rotation along the
# azimuthal direction

psd2p_az = {'pow':abs(csd32),'ang':np.angle(csd32)}

psd2p_ax = {}
psd2p_ax['pow'] = np.sqrt(abs(csd24)**2*np.cos(np.deg2rad(rot))**2 + \
                          abs(csd12)**2*np.sin(np.deg2rad(rot))**2)
psd2p_ax['ang'] = np.angle(csd24)*np.cos(np.deg2rad(rot)) - \
                    np.angle(csd12)*np.sin(np.deg2rad(rot))
      
psd2p_rd = {}
psd2p_rd['pow'] = np.sqrt(abs(csd24)**2*np.sin(np.deg2rad(rot))**2 + \
                          abs(csd12)**2*np.cos(np.deg2rad(rot))**2)
psd2p_rd['ang'] = np.angle(csd24)*np.sin(np.deg2rad(rot)) + \
                    np.angle(csd12)*np.cos(np.deg2rad(rot))

#%%
## COMPUTE PSD2Ps

komega_binning.f(fRFT,psd2p_az['ang'],psd2p_az['pow'],fRFTbin,np.arange(-np.pi,np.pi,np.deg2rad(dk)))









