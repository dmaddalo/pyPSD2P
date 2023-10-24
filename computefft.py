import numpy as np
from scipy import fft

def f(t,s):
    if not t.shape[0] % 2 == 0:
        t = t[0:-1]
        s = s[0:-1,:]

    n = t.shape[0]
    m = s.shape[1]
    
    fs = 1/(t[1]-t[0])
    fres = fs/t.shape[0]
    f = fres*np.arange(-n/2,n/2)

    transform = np.zeros((n,m),dtype=np.complex_)
    for i in range(0,m):
        transform[:,i] = fft.fftshift(fft.fft(s[:,i]))/t.shape[0]

    truncation = n/2

    f = f[int(n/2):]
    transform = transform[int(n/2):,:]
    
    return f, transform


