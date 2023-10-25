import numpy as np

def f(fs1,fs2,f,*args):
    if args:
        flim = args[0]
    else:
        flim = f[-1]
        
    if len(args) > 1:
        chunks = args[1]
    else:
        chunks = 1

    
    m = np.argwhere(abs(f-flim) < f[1]-f[0])
    m = int(m[-1])
    n = fs1.shape[1]
    
    # Cut arrays
    fs1 = fs1[0:m+1,:]
    fs2 = fs2[0:m+1,:]
    f = f[0:m+1]
    # Allocate
    csd = np.zeros((m+1,n),dtype=complex)
    psd1 = np.zeros((m+1,n),dtype=complex)
    psd2 = np.zeros((m+1,n),dtype=complex)
    # Assign
    for i in range(n):
        csd[:,i] = np.multiply(fs1[:,i],np.conj(fs2[:,i]))
        psd1[:,i] = np.multiply(fs1[:,i],np.conj(fs1[:,i]))
        psd2[:,i] = np.multiply(fs2[:,i],np.conj(fs2[:,i]))
    
    csd = csd/chunks
    psd1 = psd1/chunks
    psd2 = psd2/chunks
    
    return csd,psd1,psd2,f
    
