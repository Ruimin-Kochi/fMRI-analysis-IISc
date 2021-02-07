#!/bin/sh
singularity run --cleanenv \
/home/mas/19/csanasar/fmriprep-1.4.1.simg \
/home/mas/19/csanasar/BIDS/63380023_00/ /home/mas/19/csanasar/fmriprep/63380023_00/ participant \
--fs-no-reconall --output-spaces MNI152NLin6Asym:res-2 \
--participant-label 63380023 --fs-license-file /home/mas/19/csanasar/freesurfer.txt \
--mem_mb 30000