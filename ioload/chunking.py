import numpy as np

def f(t,WaveData,chunks):
    
    chunk_l = int(np.floor(t.shape[0]/chunks))
    probes = WaveData.shape[1]
    realizations = WaveData.shape[2]

    t_c = t[0:chunk_l]

    WaveData_c = np.zeros((chunk_l,probes,realizations*chunks))

    for i in range(chunks):
        WaveData_c[:,:,realizations*i:realizations*(i+1)] = \
            WaveData[chunk_l*i:chunk_l*(i+1),:,:]
        
    return WaveData_c, t_c
