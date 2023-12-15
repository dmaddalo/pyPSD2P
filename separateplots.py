import matplotlib.pyplot as plt
from visual import plotpsd2p

def f(kk,ff,hh,stats,params):
    
    checkaz = False
    checkax = False
    checkrd = False
    
    for name in kk:
        lowstdphs = stats[name]['meanphase']-stats[name]['stdphase']
        uppstdphs = stats[name]['meanphase']+stats[name]['stdphase']
        
        if params['colorscale'] == 'log':
            plotpsd2p.flog(kk[name],ff[name],hh[name])
        elif params['colorscale'] == 'lin':
            plotpsd2p.flin(kk[name],ff[name],hh[name])
        # plt.scatter((lowstdphs)/0.01,stats[name]['fRFTbin'],s=4,marker='.',c='r')
        # plt.scatter((uppstdphs)/0.01,stats[name]['fRFTbin'],s=4,marker='.',c='r')
        plt.xlabel('$k$ [rad/m]')
        plt.ylabel('$\omega$ [Hz]')
        if name == 'az':
            plt.title('Azimuthal dispersion; \n $\dot{m}$ = '+str(params['mdot'])+ \
                      r' SCCM, $\rho$ = '+str(params['rho'])+r' mm, $\alpha$ = ' \
                      +str(params['alpha'])+' deg')
            checkaz = True
        if name == 'ax':
            plt.title('Axial dispersion; \n $\dot{m}$ = '+str(params['mdot'])+
                      r' SCCM, $\rho$ = '+str(params['rho'])+r' mm, $\alpha$ = ' \
                      +str(params['alpha'])+' deg')
            checkax = True
        if name == 'rd':
            plt.title('Radial dispersion; \n $\dot{m}$ = '+str(params['mdot'])+
                      r' SCCM, $\rho$ = '+str(params['rho'])+r' mm, $\alpha$ = ' \
                      +str(params['alpha'])+' deg')
            checkrd = True
        
        
        plt.figure()
        plt.plot(stats[name]['fRFTbin'],10**(stats[name]['meanpow']))
        # plt.plot(stats[name]['fRFTbin'],10**(stats[name]['meanpow']+stats[name]['stdpow']),c='r')
        # plt.plot(stats[name]['fRFTbin'],10**(stats[name]['meanpow']-stats[name]['stdpow']),c='r')
        plt.yscale('log')
        plt.xlim([0,params['flim']])
        plt.ylim([1e-12,1e-4])
        plt.xlabel('$\omega$ [Hz]')
        plt.ylabel('$P_{''}$ [V$^2$ s$^{-1}$]')
        if name == 'az':
            plt.title('Azimuthal cross-power spectrum; \n $\dot{m}$ = '+str(params['mdot'])+
                      r' SCCM, $\rho$ = '+str(params['rho'])+r' mm, $\alpha$ = '+str(params['alpha'])+' deg')
        if name == 'ax':
            plt.title('Axial cross-power spectrum; \n $\dot{m}$ = '+str(params['mdot'])+
                      r' SCCM, $\rho$ = '+str(params['rho'])+r' mm, $\alpha$ = '+str(params['alpha'])+' deg')
        if name == 'rd':
            plt.title('Radial cross-power spectrum; \n $\dot{m}$ = '+str(params['mdot'])+
                      r' SCCM, $\rho$ = '+str(params['rho'])+r' mm, $\alpha$ = '+str(params['alpha'])+' deg')
            
    plt.figure()
    for name in kk:
        plt.plot(stats[name]['fRFTbin'],stats[name]['coherence'])
        
    plt.xlim([0,params['flim']])
    plt.ylim([0,1])
    plt.xlabel('$\omega$ [Hz]')
    plt.title('Coherence; \n $\dot{m}$ = '+str(params['mdot'])+
              r' SCCM, $\rho$ = '+str(params['rho'])+r' mm, $\alpha$ = '+ \
              str(params['alpha'])+' deg')
    if checkaz and checkax and checkrd:
        plt.legend(('azimuthal','axial','radial'))
    elif checkaz and checkax:
        plt.legend(('azimuthal','axial'))
    elif checkaz and checkrd:
        plt.legend(('azimuthal','radial'))
    elif checkax and checkrd:
        plt.legend(('axial','radial'))
    
    #%% OLD ROUTINE
    
    # lowstdaz = stats['az']['meanphase']-stats['az']['stdphase']
    # uppstdaz = stats['az']['meanphase']+stats['az']['stdphase']
    # lowstdax = stats['ax']['meanphase']-stats['ax']['stdphase']
    # uppstdax = stats['ax']['meanphase']+stats['ax']['stdphase']
    # lowstdrd = stats['rd']['meanphase']-stats['rd']['stdphase']
    # uppstdrd = stats['rd']['meanphase']+stats['rd']['stdphase']
    
    
    # plotpsd2p.f(kk['az'],ff['az'],hh['az'])
    # plt.scatter((lowstdaz)/0.01,stats['az']['fRFTbin'],s=4,marker='.',c='r')
    # plt.scatter((uppstdaz)/0.01,stats['az']['fRFTbin'],s=4,marker='.',c='r')
    # plt.xlabel('$k$ [rad/m]')
    # plt.ylabel('$\omega$ [Hz]')
    # plt.title('Azimuthal dispersion; \n $\dot{m}$ = '+str(params['mdot'])+ \
    #           ' SCCM, $\rho$ = '+str(params['rho'])+r' mm, $\alpha$ = '+str(params['alpha'])+' deg')

    # plt.figure()
    # plt.plot(stats['az']['fRFTbin'],10**(stats['az']['meanpow']))
    # plt.plot(stats['az']['fRFTbin'],10**(stats['az']['meanpow']+stats['az']['stdpow']),c='r')
    # plt.plot(stats['az']['fRFTbin'],10**(stats['az']['meanpow']-stats['az']['stdpow']),c='r')
    # plt.yscale('log')
    # plt.xlim([0,params['flim']])
    # plt.ylim([1e-12,1e-4])
    # plt.xlabel('$\omega$ [Hz]')
    # plt.ylabel('$P_{az}$ [V$^2$ s$^{-1}$]')
    # plt.title('Azimuthal cross-power spectrum; \n $\dot{m}$ = '+str(params['mdot'])+
    #           ' SCCM, $\rho$ = '+str(params['rho'])+r' mm, $\alpha$ = '+str(params['alpha'])+' deg')


    # plotpsd2p.f(kk['ax'],ff['ax'],hh['ax'])
    # plt.scatter((lowstdax)/0.01,stats['ax']['fRFTbin'],s=4,marker='.',c='r')
    # plt.scatter((uppstdax)/0.01,stats['ax']['fRFTbin'],s=4,marker='.',c='r')
    # plt.xlabel('$k$ [rad/m]')
    # plt.ylabel('$\omega$ [Hz]')
    # plt.title('Axial dispersion; \n $\dot{m}$ = '+str(params['mdot'])+
    #           ' SCCM, $\rho$ = '+str(params['rho'])+r' mm, $\alpha$ = '+str(params['alpha'])+' deg')

    # plt.figure()
    # plt.plot(stats['ax']['fRFTbin'],10**(stats['ax']['meanpow']))
    # plt.plot(stats['ax']['fRFTbin'],10**(stats['ax']['meanpow']+stats['ax']['stdpow']),c='r')
    # plt.plot(stats['ax']['fRFTbin'],10**(stats['ax']['meanpow']-stats['ax']['stdpow']),c='r')
    # plt.yscale('log')
    # plt.xlim([0,params['flim']])
    # plt.ylim([1e-12,1e-4])
    # plt.xlabel('$\omega$ [Hz]')
    # plt.ylabel('$P_{ax}$ [V$^2$ s$^{-1}$]')
    # plt.title('Axial cross-power spectrum; \n $\dot{m}$ = '+str(params['mdot'])+
    #           ' SCCM, $\rho$ = '+str(params['rho'])+r' mm, $\alpha$ = '+str(params['alpha'])+' deg')


    # plotpsd2p.f(kk['rd'],ff['rd'],hh['rd'])
    # plt.scatter((lowstdrd)/0.01,stats['rd']['fRFTbin'],s=4,marker='.',c='r')
    # plt.scatter((uppstdrd)/0.01,stats['rd']['fRFTbin'],s=4,marker='.',c='r')
    # plt.xlabel('$k$ [rad/m]')
    # plt.ylabel('$\omega$ [Hz]')
    # plt.title('Radial dispersion; \n $\dot{m}$ = '+str(params['mdot'])+
    #           ' SCCM, $\rho$ = '+str(params['rho'])+r' mm, $\alpha$ = '+str(params['alpha'])+' deg')

    # plt.figure()
    # plt.plot(stats['rd']['fRFTbin'],10**(stats['rd']['meanpow']))
    # plt.plot(stats['rd']['fRFTbin'],10**(stats['rd']['meanpow']+stats['rd']['stdpow']),c='r')
    # plt.plot(stats['rd']['fRFTbin'],10**(stats['rd']['meanpow']-stats['rd']['stdpow']),c='r')
    # plt.yscale('log')
    # plt.xlim([0,params['flim']])
    # plt.ylim([1e-12,1e-4])
    # plt.xlabel('$\omega$ [Hz]')
    # plt.ylabel('$P_{rd}$ [V$^2$ s$^{-1}$]')
    # plt.title('Radial cross-power spectrum; \n $\dot{m}$ = '+str(params['mdot'])+
    #           ' SCCM, $\rho$ = '+str(params['rho'])+r' mm, $\alpha$ = '+str(params['alpha'])+' deg')


    # plt.figure()
    # plt.plot(stats['az']['fRFTbin'][0::2],stats['az']['coherence'][0::2])
    # plt.plot(stats['ax']['fRFTbin'][0::2],stats['ax']['coherence'][0::2])
    # plt.plot(stats['rd']['fRFTbin'][0::2],stats['rd']['coherence'][0::2])
    # plt.xlim([0,params['flim']])
    # plt.ylim([0,1])
    # plt.xlabel('$\omega$ [Hz]')
    # plt.title('Coherence; \n $\dot{m}$ = '+str(params['mdot'])+
    #           ' SCCM, $\rho$ = '+str(params['rho'])+r' mm, $\alpha$ = '+str(params['alpha'])+' deg')
    # plt.legend(('azimuthal','axial','radial'))