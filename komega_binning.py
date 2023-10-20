from general import *
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
    
    kk, ff = np.meshgrid(kbin,fbin)
    
    h = np.zeros(kk.shape)
    
    fi = np.digitize(f,fbin)
    fi = fi[np.argwhere(f<=fbin[-1])]
    fi = fi[:,0]
    fi = np.append(fi,fbin.shape[0]-1)
    
    
    k_f = np.zeros((fbin.shape))
    p_f = np.zeros((fbin.shape))
    for i in range(fi[0],fi[-1]):
        k_f[i] = np.angle(np.mean(np.exp(1j*k[fi==i+1,:])))
        p_f[i] = 10**(np.mean(np.log10(abs(p[fi==i+1,:]))))
        
    ki = np.digitize(k_f,kbin)
    
    
    for i in range(ki.shape[0]):
        h[i,ki[i]] = h[i,ki[i]] + np.sum(p_f[i])
        
        
    out = [ff,kk,h]
        
    return out
    

    
    