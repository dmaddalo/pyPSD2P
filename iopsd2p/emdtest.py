#%% THIS CODE IS NOT MEANT TO BE RUN ON ITS OWN, BUT TO BE EXECUTED IN DEBUG MODE.
# The structure is not organic and the commands within each section are not 
# totally coherent. This serves mainly as a collection of lines of code. If 
# EMD is to be applied, use debug mode and put a breakpoint right after the
# computation of the IMFs. Perform all the other commands in the console, or 
# change and run the code lines on the go.

import emd
import numpy as np
import matplotlib.pyplot as plt
from iopsd2p import computefft, csd, binpsd2p

def f(t,WaveData_f,**kwargs):
    
    # It generally takes too long to do them all at once, not recommended
    
    # for i in range(WaveData_f.shape[2]):
        # if i == 0:
        #     imfs_ref = emd.sift.mask_sift(WaveData_f[:,0,i])
        #     imfs_az = emd.sift.mask_sift(WaveData_f[:,1,i])
        #     imfs_ax = emd.sift.mask_sift(WaveData_f[:,2,i])
        # else:
        #     imfs_ref = np.dstack((imfs_ref,emd.sift.mask_sift(WaveData_f[:,0,i])))
        #     imfs_az = np.dstack((imfs_az,emd.sift.mask_sift(WaveData_f[:,1,i])))
        #     imfs_ax = np.dstack((imfs_ax,emd.sift.mask_sift(WaveData_f[:,2,i])))
    
    # Recommended to compute them one at a time, the ones you want.
    # This takes only snapshot number 1.
    imfs_ref = emd.sift.mask_sift(WaveData_f[:,0,0])
    imfs_az = emd.sift.mask_sift(WaveData_f[:,1,0])
    imfs_ax = emd.sift.mask_sift(WaveData_f[:,2,0])
        
#%% Transforms of the IMFs
    for i in range(0,imfs_ref.shape[1]):
        if i == 0:
            fRFT, imfs_ref_t = computefft.f(t,imfs_ref[:,i],returnf=True)
            imfs_az_t = computefft.f(t,imfs_az[:,i],returnf=False)
            imfs_ax_t = computefft.f(t,imfs_ax[:,i],returnf=False)
        else:
            imfs_ref_t = np.hstack((imfs_ref_t,computefft.f(t,imfs_ref[:,i],returnf=False)))
            imfs_az_t = np.hstack((imfs_az_t,computefft.f(t,imfs_az[:,i],returnf=False)))
            imfs_ax_t = np.hstack((imfs_ax_t,computefft.f(t,imfs_ax[:,i],returnf=False)))

#%% Visualize the IMFs
    emd.plotting.plot_imfs(imfs_az)

#%% Visualize the IMF Fourier transforms
    plt.figure()
    for i in range(imfs_ref_t.shape[1]):
        plt.subplot(imfs_ref_t.shape[1],1,i+1)
        plt.plot(fRFT,abs(imfs_ref_t[:,i]))
        plt.xlim([0,2e5])
        plt.yscale('log')
        plt.ylim([1e-7,1e-3])
    
#%% Generic routine to visualize the dispersion plot of one IMF or the sum of any number

    # Transform of sum of IMFs from 5 (included) to 9 (not included)
    imfsum = np.sum(imfs_az[:,5:9],axis=1)
    
    # Transform of specific IMF number 4 (n+1)
    csdaz,_,_,_ = csd.f(imfs_az_t[:,3],imfs_ref_t[:,3],fRFT)
    # csdax,_,_,_ = csd.f(imfs_ax_t[:,i],imfs_ref_t[:,i],fRFT)
        
    kkaz,ffaz,hhaz = binpsd2p.f(fRFT,np.angle(csdaz),abs(csdaz),fRFTbin,
                            np.arange(-np.pi,np.pi,np.deg2rad(dk)))
        
#%% Compute instantaneous frequency and amplitude
    IP, IF, IA = emd.spectra.frequency_transform(imfs_ref,1/t[1],'nht')
    IPaz, IFaz, IAaz = emd.spectra.frequency_transform(imfs_az,1/t[1],'nht')
    IPax, IFax, IAax = emd.spectra.frequency_transform(imfs_ax,1/t[1],'nht')
    
    # It is interesting to plot the instantaneous phase difference between
    # two specific modes that are of interest. For instance, the azimuthal IMF 
    # at 75 kHz is generally number 4 (3 in Python indexing), for which the 
    # value (IPaz-IP)/0.01 returns the azimuthal wavenumber k_\theta for that
    # specific IMF. These values will span from -2pi to 2pi but I suppose this
    # is an artifact and the actual values should only go from -pi to pi. By
    # averaging out only the values between -pi and pi, the average value of 
    # the difference between the two instantaneous phases is coherent with the
    # wavenumbers provided by the dispersion plots. Plotting them with respect
    # to the time vector will provide the wavenumber temporal evolution.
    k_az = (IPaz - IP)/0.01
    k_ax = (IPax - IP)/0.01
    
    # Remove the artifacts above pi and below -pi (take the indexes of -pi<k<pi)
    truek_az = list()
    truek_ax = list()
    for i in range(k_az.shape[1]):
        truek_az.append(np.transpose(np.where(np.logical_and(k_az[:,i]<314,
                                                           k_az[:,i]>-314))))
        truek_ax.append(np.transpose(np.where(np.logical_and(k_ax[:,i]<314,
                                                           k_ax[:,i]>-314))))
        
    for i in range(k_az.shape[1]):
        print(np.mean(k_az[truek_az[i],i]))
    
    for i in range(k_ax.shape[1]):
        print(np.mean(k_ax[truek_ax[i],i]))
        
    plt.figure()
    plt.plot(t[truek_az[4]],k_az[truek_az[4],4])
    plt.xlim([0.08,0.081])
    
    plt.figure()
    plt.plot(t[truek_az[8]],k_az[truek_az[8],8])
    plt.xlim([0.08,0.081])

#%% Compute Hilbert-Huang transform
    f, hht = emd.spectra.hilberthuang(IF,IA,(0, 2e5, 101),mode='amplitude',
                                      sum_time=False)
    
#%% Plot Hilbert-Huang spectrum
    
    # Add a little smoothing to help visualisation
    shht = ndimage.gaussian_filter(hht,1)
    
    plt.figure()
    plt.pcolormesh(t[:1600:],f,shht[:,:1600:,],norm = colors.LogNorm(vmin=1e-4,vmax=1e-0),
                   cmap='hot_r')
    
    return imfs_ref,imfs_az, imfs_ax