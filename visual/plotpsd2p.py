import matplotlib.pyplot as plt
import matplotlib.colors as colors

def f(kk,ff,hh):
    plt.figure()
    plt.pcolor(kk/0.01,ff,hh,
               norm = colors.LogNorm(vmin=1e-11,vmax=1e-4),
               cmap = 'jet',shading='auto')
    plt.colorbar()

    ## (SHITTY) WAY TO SET COLORBAR LIMITS AFTER PLOTTING EVERYTHING
    # plt.figure(1).get_children()[1].get_children()[0].set_clim(vmin=,vmax=)
