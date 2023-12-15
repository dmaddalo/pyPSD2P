#%% IMPORT
# from general import *
from ioload import chunking, definefolder, wfm2mat
from visual import plotpsd2p
from iopsd2p import binpsd2p, computefft,computestats, csd
import matplotlib.pyplot as plt
import numpy as np

class structured:
    def __getattr__(self,name):
        self.__dict__[name] = structured()
        return self.__dict__[name]


#%% SLIDESHOW
# for i in range(0,WaveData.shape[2]):
#     plt.figure(2).clear()
#     plt.pcolor(z,r,WaveData[:,:,i],cmap='jet',shading='auto')
#     plt.pause(0.1)
#%%

df = 400
flim = 2e5

directory = definefolder.fsim()

WaveData,t,z,r = wfm2mat.fsim(directory)

WaveData_f = WaveData - np.mean(WaveData,axis=2,keepdims=True)

sx = np.array([WaveData_f[17,21,:],WaveData_f[17,25,:],WaveData_f[11,21,:]]).transpose()

temp = []
for i in range(0,sx.shape[1]):
    temp.append(computefft.f(t,sx[:,i]))

    if i == 0:
        WaveData_t = temp[i][1]
        fRFT = temp[i][0]
    else:
        WaveData_t = np.hstack((WaveData_t,temp[i][1]))
    
del temp

fRFTbin = np.arange(fRFT[0],flim+df,df)

csd12,psd2,psd1,_ = csd.f(WaveData_t[:,1],WaveData_t[:,0],fRFT)

csd13,psd3,_,_ = csd.f(WaveData_t[:,2],WaveData_t[:,0],fRFT)


csdax = {'pow':abs(csd12),'ang':np.angle(csd12),'orig':csd12}

csdrd = {'pow':abs(csd13),'ang':np.angle(csd13),'orig':csd13}


kkax,ffax,hhax = binpsd2p.f(fRFT,csdax['ang'],csdax['pow'],fRFTbin,
                        np.arange(-np.pi,np.pi,np.deg2rad(1)))

kkrd,ffrd,hhrd = binpsd2p.f(fRFT,csdrd['ang'],csdrd['pow'],fRFTbin,
                        np.arange(-np.pi,np.pi,np.deg2rad(1)))
    

statsax = computestats.f(csdax,psd1,psd2,fRFT,df,flim)

statsrd = computestats.f(csdrd,psd1,psd3,fRFT,df,flim)


mscax = abs(statsax['coherence']**2)
mscrd = abs(statsrd['coherence']**2)
statsax['coherence'] = mscax
statsrd['coherence'] = mscrd


plotpsd2p.flog(kkax,ffax,hhax)
plt.title('Axial dispersion')
# lowstdaz = statsax['meanphase']-statsax['stdphase']
# uppstdaz = statsax['meanphase']+statsax['stdphase']
# plt.scatter(lowstdaz/0.01,statsax['fRFTbin'],s=4,marker='.',c='r')
# plt.scatter(uppstdaz/0.01,statsax['fRFTbin'],s=4,marker='.',c='r')

plt.figure()
plt.plot(fRFTbin,statsax['meanpow'])
plt.title('Axial cross-power')

plt.figure()
plt.plot(fRFTbin,statsax['coherence'])
plt.title('Axial coherence')


plotpsd2p.f(kkrd,ffrd,hhrd)
plt.title('Radial dispersion')
# lowstdaz = statsax['meanphase']-statsax['stdphase']
# uppstdaz = statsax['meanphase']+statsax['stdphase']
# plt.scatter(lowstdaz/0.01,statsax['fRFTbin'],s=4,marker='.',c='r')
# plt.scatter(uppstdaz/0.01,statsax['fRFTbin'],s=4,marker='.',c='r')

plt.figure()
plt.plot(fRFTbin,statsrd['meanpow'])
plt.title('Radial cross-power')

plt.figure()
plt.plot(fRFTbin,statsrd['coherence'])
plt.title('Radial coherence')