import matplotlib.pyplot as plt
from visual import plotpsd2p

def f(kk,ff,hh,stats,params):
    lowstdaz = stats['az']['meanphase']-stats['az']['stdphase']
    uppstdaz = stats['az']['meanphase']+stats['az']['stdphase']
    lowstdax = stats['ax']['meanphase']-stats['ax']['stdphase']
    uppstdax = stats['ax']['meanphase']+stats['ax']['stdphase']
    lowstdrd = stats['rd']['meanphase']-stats['rd']['stdphase']
    uppstdrd = stats['rd']['meanphase']+stats['rd']['stdphase']
    
    
    plotpsd2p.f(kk['az'],ff['az'],hh['az'])
    plt.scatter((lowstdaz)/0.01,stats['az']['fRFTbin'],s=4,marker='.',c='r')
    plt.scatter((uppstdaz)/0.01,stats['az']['fRFTbin'],s=4,marker='.',c='r')
    plt.xlabel('$k$ [rad/s]')
    plt.ylabel('$\omega$ [Hz]')
    plt.title('Azimuthal dispersion; \n $\dot{m}$ = '+str(params['mdot'])+ \
              ' SCCM, $d$ = '+str(params['d'])+r' mm, $\alpha$ = '+str(params['alpha'])+' deg')

    plt.figure()
    plt.plot(stats['az']['fRFTbin'],10**(stats['az']['meanpow']))
    plt.plot(stats['az']['fRFTbin'],10**(stats['az']['meanpow']+stats['az']['stdpow']),c='r')
    plt.plot(stats['az']['fRFTbin'],10**(stats['az']['meanpow']-stats['az']['stdpow']),c='r')
    plt.yscale('log')
    plt.xlim([0,1e5])
    plt.ylim([1e-11,1e-4])
    plt.xlabel('$\omega$ [Hz]')
    plt.ylabel('$P_{az}$ [V$^2$ s$^{-1}$]')
    plt.title('Azimuthal cross-power spectrum; \n $\dot{m}$ = '+str(params['mdot'])+
              ' SCCM, $d$ = '+str(params['d'])+r' mm, $\alpha$ = '+str(params['alpha'])+' deg')


    plotpsd2p.f(kk['ax'],ff['ax'],hh['ax'])
    plt.scatter((lowstdax)/0.01,stats['ax']['fRFTbin'],s=4,marker='.',c='r')
    plt.scatter((uppstdax)/0.01,stats['ax']['fRFTbin'],s=4,marker='.',c='r')
    plt.xlabel('$k$ [rad/s]')
    plt.ylabel('$\omega$ [Hz]')
    plt.title('Axial dispersion; \n $\dot{m}$ = '+str(params['mdot'])+
              ' SCCM, $d$ = '+str(params['d'])+r' mm, $\alpha$ = '+str(params['alpha'])+' deg')

    plt.figure()
    plt.plot(stats['ax']['fRFTbin'],10**(stats['ax']['meanpow']))
    plt.plot(stats['ax']['fRFTbin'],10**(stats['ax']['meanpow']+stats['ax']['stdpow']),c='r')
    plt.plot(stats['ax']['fRFTbin'],10**(stats['ax']['meanpow']-stats['ax']['stdpow']),c='r')
    plt.yscale('log')
    plt.xlim([0,1e5])
    plt.ylim([1e-11,1e-4])
    plt.xlabel('$\omega$ [Hz]')
    plt.ylabel('$P_{ax}$ [V$^2$ s$^{-1}$]')
    plt.title('Axial cross-power spectrum; \n $\dot{m}$ = '+str(params['mdot'])+
              ' SCCM, $d$ = '+str(params['d'])+r' mm, $\alpha$ = '+str(params['alpha'])+' deg')


    plotpsd2p.f(kk['rd'],ff['rd'],hh['rd'])
    plt.scatter((lowstdrd)/0.01,stats['rd']['fRFTbin'],s=4,marker='.',c='r')
    plt.scatter((uppstdrd)/0.01,stats['rd']['fRFTbin'],s=4,marker='.',c='r')
    plt.xlabel('$k$ [rad/s]')
    plt.ylabel('$\omega$ [Hz]')
    plt.title('Radial dispersion; \n $\dot{m}$ = '+str(params['mdot'])+
              ' SCCM, $d$ = '+str(params['d'])+r' mm, $\alpha$ = '+str(params['alpha'])+' deg')

    plt.figure()
    plt.plot(stats['rd']['fRFTbin'],10**(stats['rd']['meanpow']))
    plt.plot(stats['rd']['fRFTbin'],10**(stats['rd']['meanpow']+stats['rd']['stdpow']),c='r')
    plt.plot(stats['rd']['fRFTbin'],10**(stats['rd']['meanpow']-stats['rd']['stdpow']),c='r')
    plt.yscale('log')
    plt.xlim([0,1e5])
    plt.ylim([1e-11,1e-4])
    plt.xlabel('$\omega$ [Hz]')
    plt.ylabel('$P_{rd}$ [V$^2$ s$^{-1}$]')
    plt.title('Radial cross-power spectrum; \n $\dot{m}$ = '+str(params['mdot'])+
              ' SCCM, $d$ = '+str(params['d'])+r' mm, $\alpha$ = '+str(params['alpha'])+' deg')


    plt.figure()
    plt.plot(stats['az']['fRFTbin'],stats['az']['coherence'])
    plt.plot(stats['ax']['fRFTbin'],stats['ax']['coherence'])
    plt.plot(stats['rd']['fRFTbin'],stats['rd']['coherence'])
    plt.xlim([0,1e5])
    plt.ylim([0,1])
    plt.xlabel('$\omega$ [Hz]')
    plt.title('Coherence; \n $\dot{m}$ = '+str(params['mdot'])+
              ' SCCM, $d$ = '+str(params['d'])+r' mm, $\alpha$ = '+str(params['alpha'])+' deg')
    plt.legend(('azimuthal','axial','radial'))
