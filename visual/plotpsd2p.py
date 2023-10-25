import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors

def f(kk,ff,hh):
    plt.figure()
    plt.pcolor(kk/0.01,ff,hh,
               norm = colors.LogNorm(vmin=1e-11,vmax=1e-4),
               cmap = 'jet',shading='auto')
    plt.colorbar()
