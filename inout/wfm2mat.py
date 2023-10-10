from general import os, np
import pandas as pd

def f(directory):
    # files = glob.glob(os.path.join(directory,'*.txt'))
    i = 1
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            # with open(os.path.join(directory,filename),'r') as file:
                # alldata = [line.strip() for line in file.readlines()]
            tempdata = pd.read_csv(os.path.join(directory,filename),sep='\t',header=24)
            # trial = np.array(alldata[24:-1])
            # WaveData = np.array(tempdata)
    # return realization
