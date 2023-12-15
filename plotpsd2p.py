import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib as mpl
import numpy as np

def flog(kk,ff,hh):
    plt.figure()
    plt.pcolor(kk/0.01,ff,hh,
               norm = colors.LogNorm(vmin=1e-11,vmax=1e-4),
               cmap = 'jet',shading='auto')
    plt.colorbar()
    
    
def flin(kk,ff,hh):
    
    jet = mpl.cm.jet(np.arange(256))
    wjet = np.vstack(([1,1,1,1],jet))
    wjet = colors.ListedColormap(wjet,name='wjet',N=wjet.shape[0])
    
    plt.figure()
    plt.pcolor(kk/0.01,ff,hh,
               vmin=0,vmax=1,cmap=wjet,shading='auto')
    plt.colorbar()
    
    ## (SHITTY) WAY TO SET COLORBAR LIMITS AFTER PLOTTING EVERYTHING
    # plt.figure(1).get_children()[1].get_children()[0].set_clim(vmin=,vmax=)
