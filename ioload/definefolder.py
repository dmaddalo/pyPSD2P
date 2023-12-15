from general import os

def f(mdot,rho,alpha,*args):
    # Recover information
    lang = args[0]
    day = args[1]
    opsparent = args[2]
    opschild = args[3]
    
    ## Root folder
    # root = ''
    root = os.path.normpath(os.getcwd()+os.sep+os.pardir)

    ## Define final directory
    additional = os.path.normpath('datasets/'+ lang + os.sep + day)
    
    ## Final directory
    directory = os.path.normpath(str(root + os.sep + additional + os.sep + opsparent +
                                 os.sep + '{:.1f}'.format(mdot) + '_' + 
                                 '{:03d}'.format(rho) + '_' + 
                                 '{:02d}'.format(alpha) + 
                                 os.sep + opschild))
    
    ## Special cases
    if opsparent == 'noplasmamwoff' or opsparent == 'noplasmamwon':
        directory = os.path.normpath(str(root + os.sep + additional + os.sep +
                                     opsparent))

    return directory

#%% For HETs simulation dataset. Called by 'mainsim.py'

def fsim():
    ## Root folder
    root = os.path.normpath(os.getcwd()+os.sep+os.pardir)
    
    additional = os.path.normpath('datasets/A_simHET/SPT100_Vd300_mdot5')
    
    directory = os.path.normpath(root + os.sep + additional)
    
    return directory

#%% For camera dataset (Victor). Called by 'maincam.py'

def fcam():
    
    root = root = os.path.normpath(os.getcwd()+os.sep+os.pardir)
    
    additional = os.path.normpath('datasets/fixedlang/26.10')
    
    directory = os.path.normpath(root + os.sep + additional)
    
    return directory