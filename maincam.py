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

df = 500
flim = 1e5

directory = definefolder.fcam()

WaveData,t = wfm2mat.fcam(directory)

WaveData_f = WaveData - np.mean(WaveData,axis=0,keepdims=True)

temp = []
for i in range(0,WaveData.shape[1]):
    temp.append(computefft.f(t,WaveData[:,i]))

    if i == 0:
        WaveData_t = temp[i][1]
        fRFT = temp[i][0]
    else:
        WaveData_t = np.hstack((WaveData_t,temp[i][1]))
    
del temp

fRFTbin = np.arange(fRFT[0],flim+df,df)

#%%
csd15,psd1,psd5,_ = csd.f(WaveData_t[:,0],WaveData_t[:,4],fRFT)

csd15 = {'pow':abs(csd15),'ang':np.angle(csd15),'orig':csd15}

kk15,ff15,hh15 = binpsd2p.f(fRFT,csd15['ang'],csd15['pow'],fRFTbin,
                        np.arange(-np.pi,np.pi,np.deg2rad(1)))

stats15 = computestats.f(csd15,psd1,psd5,fRFT,df,flim)
stats15['coherence'] = abs(stats15['coherence']**2)

#%%
csd26,psd2,psd6,_ = csd.f(WaveData_t[:,1],WaveData_t[:,5],fRFT)

csd26 = {'pow':abs(csd26),'ang':np.angle(csd26),'orig':csd26}

kk26,ff26,hh26 = binpsd2p.f(fRFT,csd26['ang'],csd26['pow'],fRFTbin,
                        np.arange(-np.pi,np.pi,np.deg2rad(1)))

stats26 = computestats.f(csd26,psd2,psd6,fRFT,df,flim)
stats26['coherence'] = abs(stats26['coherence']**2)

#%%
csd37,psd3,psd7,_ = csd.f(WaveData_t[:,2],WaveData_t[:,6],fRFT)

csd37 = {'pow':abs(csd37),'ang':np.angle(csd37),'orig':csd37}

kk37,ff37,hh37 = binpsd2p.f(fRFT,csd37['ang'],csd37['pow'],fRFTbin,
                        np.arange(-np.pi,np.pi,np.deg2rad(1)))

stats37 = computestats.f(csd37,psd3,psd7,fRFT,df,flim)
stats37['coherence'] = abs(stats37['coherence']**2)

#%%
csd48,psd4,psd8,_ = csd.f(WaveData_t[:,3],WaveData_t[:,7],fRFT)

csd48 = {'pow':abs(csd48),'ang':np.angle(csd48),'orig':csd48}

kk48,ff48,hh48 = binpsd2p.f(fRFT,csd48['ang'],csd48['pow'],fRFTbin,
                        np.arange(-np.pi,np.pi,np.deg2rad(1)))

stats48 = computestats.f(csd48,psd4,psd8,fRFT,df,flim)
stats48['coherence'] = abs(stats48['coherence']**2)

#%%
plotpsd2p.flog(kk15,ff15,hh15)

plt.figure()
plt.plot(fRFTbin,stats15['meanpow'])

plt.figure()
plt.plot(fRFTbin,stats15['coherence'])

#%%
plotpsd2p.flog(kk26,ff26,hh26)

plt.figure()
plt.plot(fRFTbin,stats26['meanpow'])

plt.figure()
plt.plot(fRFTbin,stats26['coherence'])

#%%
plotpsd2p.flog(kk37,ff37,hh37)

plt.figure()
plt.plot(fRFTbin,stats37['meanpow'])

plt.figure()
plt.plot(fRFTbin,stats37['coherence'])

#%%
plotpsd2p.flog(kk48,ff48,hh48)

plt.figure()
plt.plot(fRFTbin,stats48['meanpow'])

plt.figure()
plt.plot(fRFTbin,stats48['coherence'])

