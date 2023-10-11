# %%
from general import *
from inout import *

# %%
## DEFINE

## d = axial distance [mm]
d = 20
## alpha = angular displacement [deg]
alpha = 0
## SCCMz
mdot = 1
##
forced = 0
day = '5.10'
## Number of chunks in which to divide the waveform
chunks = 10
## Binning parameters (none of those depend on the dataset)
df = 200       # Hz
dk = 3         # deg
flim = 1e5     # upper limit frequency

# %%
## INPUT OUTPUT

directory = definefolder.f(mdot,d,alpha,day)

if forced:
    directory = directory+"-forced"

WaveData, t = wfm2mat.f(directory)

chunking.f(t,WaveData,chunks)

# %%
