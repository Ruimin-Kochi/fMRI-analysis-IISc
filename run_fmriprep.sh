#!/bin/sh

subj = $1
nvidia-docker run --name $SLURM_JOB_ID --user $(id -u $USER):$(id -g $USER) --rm \
	-v /etc/passwd:/etc/passwd \
	-v /etc/group:/etc/group \
	-v /etc/shadow:/etc/shadow \
	-v /home/mas/19/csanasar/BIDS/$subj:/data:ro \
	-v /home/mas/19/csanasar/fmriprep2:/out \
	-v /home/mas/19/csanasar/batch_work:/work \
	poldracklab/fmriprep:latest \
	/data /out/$subj \
	participant \
	-w /work \
	--participant_label $subj \
	--fs-license-file /work/freesurfer.txt \
	--fs-no-reconall --output-spaces MNI152NLin6Asym:res-2