from general import os, pathlib

def f(mdot,d,alpha,*args):
    # ROOT FOLDER
    # root = ''
    root = os.path.normpath(os.getcwd()+os.sep+os.pardir)

    ## Define final directory
    if args:
        additional = os.path.normpath('datasets/prelim/'+args[0])
    else:
        additional = os.path.normpath('datasets/prelim')

    directory = os.path.normpath(str(root + os.sep +  additional + '/' + \
    '{:.1f}'.format(mdot) + '_' + '{:03d}'.format(d) + '_' + \
    '{:02d}'.format(alpha)))
    
    return directory