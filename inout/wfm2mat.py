from general import os, np
import pandas as pd

def f(directory):
    # files = glob.glob(os.path.join(directory,'*.txt'))
    i = 0
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            # with open(os.path.join(directory,filename),'r') as file:
                # alldata = [line.strip() for line in file.readlines()]
            tempdata = np.array(pd.read_csv(os.path.join \
                    (directory,filename),sep='\t',header=23))
            # trial = np.array(alldata[24:-1])
            if i == 0:
                WaveData = tempdata[...,np.newaxis]
            else:
                WaveData = np.dstack((WaveData,tempdata))
            i += 1

    print('okay')
    # return realization