#!/bin/sh
#SBATCH --job-name=friprep_test2              # Job name
#SBATCH --ntasks=1                                                 # Run on a single CPU
#SBATCH --time=24:00:00                                   # Time limit hrs:min:sec
#SBATCH --gres=gpu:1
#SBATCH --partition=q_1day-4G
#SBATCH --output=log/%x-%A-%a.out
pwd; hostname; date |tee result

nvidia-docker run --name $SLURM_JOB_ID --user $(id -u $USER):$(id -g $USER) --rm \
	-v /etc/passwd:/etc/passwd \
	-v /etc/group:/etc/group \
	-v /etc/shadow:/etc/shadow \
	-v /home/mas/19/csanasar/BIDS/63380023_00:/data:ro \
	-v /home/mas/19/csanasar/fmriprep2:/out \
	-v /home/mas/19/csanasar/batch_work:/work \
	poldracklab/fmriprep:latest \
	/data /out/63380023_00 \
	participant \
	-w /work \
	--participant_label 63380023 \
	--fs-license-file /work/freesurfer.txt \
	--fs-no-reconall --output-spaces MNI152NLin6Asym:res-2