from general import *
from inout import *

## d = axial distance [mm]
d = 140
## alpha = angular displacement [deg]
alpha = 50
## SCCMz
mdot = 1
##
forced = 0
day = '5.10'
## Number of chunks in which to divide the waveform
chunks = 20
## Binning parameters (none of those depend on the dataset)
df = 200       # Hz
dk = 3         # deg
flim = 1e5     # upper limit frequency

directory = definefolder.f(mdot,d,alpha,day)

wfm2mat.f(directory)

