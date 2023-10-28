import numpy as np

def f(csdij,psdi,psdj,f,df,flim):
    
    fbin = np.arange(f[0],flim+df,df)
    
    if f[-1] >= fbin[-1]+df:
        fx = np.where(abs(f-fbin[-1]-fbin[1]) == min(abs(f-fbin[-1]-fbin[1])))[0][0]
    else:
        fx = f.shape[0]
        
    f = f[0:fx]
    
    fi = np.digitize(f,fbin)
    
    powercsd = csdij['pow'][0:fx,:]
    phasecsd = csdij['ang'][0:fx,:]
    origcsd = csdij['orig'][0:fx,:]
    psdi = psdi[0:fx,:]
    psdj = psdj[0:fx,:]
    
    stats = {'meanphase':np.zeros((fi[-1])),'stdphase':np.zeros((fi[-1])),
             'meanpow':np.zeros((fi[-1])),'stdpow':np.zeros((fi[-1])),
             'coherence':np.zeros((fi[-1]),dtype=complex),'fRFTbin':fbin}
    for i in range(0,fi[-1]):
        stats['meanphase'][i] = np.angle(np.mean(np.exp(1j*phasecsd[fi==i+1,:])))
        stats['stdphase'][i] = np.mean(np.pi-abs(np.pi - abs(phasecsd[fi==i+1,:] + \
                             - stats['meanphase'][i])))
            
        stats['meanpow'][i] = np.mean(np.log10(powercsd[fi==i+1,:]))
        stats['stdpow'][i] = np.std(np.log10(powercsd[fi==i+1,:]),ddof=1)
        
        stats['coherence'][i] = np.sum(origcsd[fi==i+1,:]) / \
                           ( np.sqrt(np.sum(psdi[fi==i+1]))*np.sqrt(np.sum(psdj[fi==i+1])) )
        
    return stats
    
    
