import os
import argparse
import shutil
import subprocess
import json
import warnings

from multiprocessing import Pool

import pandas as pd
import numpy as np
from os.path import abspath, join, pardir

from nilearn import datasets
# from roi_mean_sub import roi_mean_interface
from bids.layout import BIDSLayout
from nipype.pipeline import Node, MapNode, Workflow
from nipype.interfaces.io import DataSink, DataGrabber
from nipype.algorithms.confounds import TSNR
from nipype.interfaces.utility import Function, IdentityInterface
from nilearn.input_data import NiftiLabelsMasker
from nipype.interfaces import fsl
from nipype.interfaces.utility import Rename
from nilearn import image, plotting, signal
from nilearn.connectome import ConnectivityMeasure
from nilearn.input_data import NiftiLabelsMasker
import nibabel as nib

base_dir = "/home/connoi/Downloads/Nabarun"

def _run_copy(source, output_path):
    cmd_str = "cp -r {} {}".format(source, output_path)
    print(cmd_str)
    subprocess.run(cmd_str, shell=True)

def _run_untar(outdir, srcfile):
    cmd_str = "tar -C {} -zxf {}".format(outdir, srcfile)
    print(cmd_str)
    subprocess.run(cmd_str, shell=True)

def _rm_tar(srcfile):
    cmd_str = "rm -rf {}".format(srcfile)
    print(cmd_str)
    subprocess.run(cmd_str, shell=True)

def _scp_fmriprep(srcfile, base_dir):
    cmd_str = "scp -q -r nabarun@10.36.17.186:~/RADC/sym_radc/fmriprep/{} {}/RADC/fmriprep".format(srcfile, base_dir)
    print(cmd_str)
    subprocess.run(cmd_str, shell=True)

def collect_data(layout, participant_label, bids_validate=True):
    queries = {
        "func": {"datatype": "func", "suffix": "bold"},
        "confounds": {"datatype": "func", "suffix": ['timeseries','regressors']},
        "flair": {"datatype": "anat", "suffix": "FLAIR"},
        "t2w": {"datatype": "anat", "suffix": "T2w"},
        "t1w": {"datatype": "anat", "suffix": "T1w"},
        "roi": {"datatype": "anat", "suffix": "roi"},
    }

    subj_data = {
        dtype: sorted(
            layout.get(
                return_type="file",
                subject=participant_label,
                extension=["nii", "nii.gz", "tsv"],
                **query
            )
        )
        for dtype, query in queries.items()
    }

    return subj_data

def extract_confounds(confound_file, confound_vars):
    confound_df = pd.read_csv(confound_file, delimiter='\t')
    confound_df = confound_df[confound_vars]
    for col in confound_df.columns:

        #Example X --> X_dt
        new_name = '{}_dt'.format(col)

        #Compute differences for each pair of rows from start to end.
        new_col = confound_df[col].diff()

        #Make new column in our dataframe
        confound_df[new_name] = new_col
    return confound_df.values

df = pd.read_csv(base_dir+'/fmriprep_list', header=None)

dataset = datasets.fetch_atlas_schaefer_2018(n_rois=1000, yeo_networks=7, 
                            resolution_mm=1)
atlas_filename = dataset.maps
labels = dataset.labels
masker = NiftiLabelsMasker(labels_img=atlas_filename, standardize=True,
                           memory='nilearn_cache', verbose=0)
  
pool = Pool()

# for subject_id in df[0]:
def f(subject_id):
    print("Target: {}\n".format(subject_id))
    _scp_fmriprep(subject_id, base_dir)

    layout = BIDSLayout('RADC/fmriprep/'+subject_id,validate=False)
    subjects = layout.get_subjects()
    print(subjects)
    
    pooled_subjects = []
    tr_drop = 4

    for sub in subjects:
        #Get functional file and confounds file
        subj_data = collect_data(layout, sub, False)
        func_file = subj_data['func'][0]
        confound_file = subj_data['confounds'][0]

        #Load functional file and perform TR drop
        func_img = image.load_img(func_file)
        func_img = func_img.slicer[:,:,:,tr_drop+1:]

        #Convert cnfounds file into required format
        confound_vars = ['trans_x', 'trans_y', 'trans_z', 
                        'rot_x', 'rot_y', 'rot_z',
                        'global_signal','a_comp_cor_01','a_comp_cor_02']
        confounds = extract_confounds(confound_file, confound_vars)

        #Drop TR on confound matrix
        confounds = confounds[tr_drop+1:,:]
        #Apply cleaning, parcellation and extraction to functional data
        time_series = masker.fit_transform(func_img,confounds)
        pooled_subjects.append(time_series)
        np.save(base_dir+'/RADC/schaefer_pooled_subjects/'+subject_id, time_series)
        print("Timeseries saved with shape",np.shape(time_series))
        correlation_measure = ConnectivityMeasure(kind='correlation')
        correlation_matrix = correlation_measure.fit_transform(pooled_subjects)
        np.save(base_dir+'/RADC/schaefer_pooled_correlation_matrices/'+subject_id, correlation_matrix)
        print("Corr matrix saved with shape",np.shape(correlation_matrix))

    _rm_tar("{}/RADC/fmriprep/{}".format(base_dir, subject_id))
    print("\n")

p = Pool()
p.map(f, df[0])