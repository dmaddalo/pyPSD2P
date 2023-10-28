import numpy as np
from scipy import fft

def f(f,k,p,fbin,kbin):
    # # Ensure column vectors
    # fbin = fbin(:)
    # kbin = kbin(:)
    # # If these are matrices, isrow(...) returns false
    # if isrow(f)
    #     f = f(:)
    # if isrow(k)
    #     k = k(:)
    # if isrow(p) 
    #     p = p(:)
    
    if f.ndim == 1:
        f = f[...,None]
    if k.ndim == 1:
        k = k[...,None]
    if p.ndim == 1:
        p = p[...,None]
    
    kk, ff = np.meshgrid(kbin,fbin)
    
    h = np.zeros(kk.shape)
    
    if f[-1] >= fbin[-1]+fbin[1]:
        fx = np.where(abs(f-fbin[-1]-fbin[1]) == min(abs(f-fbin[-1]-fbin[1])))[0][0]
    else:
        fx = f.shape[0]
        
    f = f[0:fx,0]
    k = k[0:fx,:]
    p = p[0:fx,:]
    
    fi = np.digitize(f,fbin)
    
    # fbinc = np.append(fbin,fbin[-1]+fbin[1])
    # fi = np.digitize(f,fbinc)
    # # fi = fi[np.argwhere(fi<fi[-1])]
    # fi = fi[0:np.argmax(fi == np.unique(fi)[-2])+1]
    # # fi = fi[0:-1,0]
    
    
    k_f = np.zeros((fbin.shape))
    p_f = np.zeros((fbin.shape))
    for i in range(0,fi[-1]):
        k_f[i] = np.angle(np.mean(np.exp(1j*k[fi==i+1,:])))
        p_f[i] = 10**(np.mean(np.log10(abs(p[fi==i+1,:]))))
        
    ki = np.digitize(k_f,kbin)
    
    for i in range(ki.shape[0]):
        h[i,ki[i]] = h[i,ki[i]] + np.sum(p_f[i])
        
    return kk,ff,h
    

    
    
