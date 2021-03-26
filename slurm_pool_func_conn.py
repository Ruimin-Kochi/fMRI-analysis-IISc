import os
import argparse
import shutil
import subprocess
import json
import warnings
import sys, glob

from multiprocessing import Pool

import pandas as pd
import numpy as np


data_dir = "/home/scratch/nabaruns/outcorr"
df = pd.read_csv("/home/nabaruns/corr_done.txt",header=None)
print(df.head())

pooled_corr_mat=[]
for f in df[0]:
    corr_mat = np.load(os.path.join(data_dir,f+".npy"))
    pooled_corr_mat.append(corr_mat[0])
print(np.shape(pooled_corr_mat))
np.save(os.path.join(data_dir,"pooled_corr_mat"), pooled_corr_mat)