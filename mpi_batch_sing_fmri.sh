#!/bin/sh
#PBS -N fmriprep
#PBS -l nodes=1:ppn=16:debug
#PBS -l walltime=02:00:00
#PBS -o /home/mas/19/csanasar/${PBS_JOBNAME}.o${PBS_JOBID} 
#PBS -e /home/mas/19/csanasar/${PBS_JOBNAME}.e${PBS_JOBID}
pwd; hostname; date |tee result

cd /home/mas/19/csanasar
NPROCS=`wc -l < $PBS_NODEFILE`
HOSTS=`cat $PBS_NODEFILE | uniq | tr ‘\n’ “,” | sed ‘s|,$||’`
# echo $PBS_NODEFILE $NPROCS $HOSTS > mpising/output1.log
# # mpirun -n <NUMBER_OF_RANKS> singularity exec <PATH/TO/MY/IMAGE>
# # mpiexec -np $NPROCS –host $HOSTS singularity > mpising/output.log
# setenv SINGULARITYENV_TEMPLATEFLOW_HOME /home/mas/19/csanasar/templateflow/
# module use singularity
# module load
cmd="/usr/local/bin/singularity run --cleanenv \
-B /home/mas/19/csanasar/:/data \
/data/fmriprep-1.4.1.simg \
/data/BIDS/78916544_00/ /data/fmriprep/78916544_00/ participant \
--fs-no-reconall --output-spaces MNI152NLin6Asym:res-2 \
--participant-label 78916544 --fs-license-file /data/freesurfer.txt"
# echo mpirun -np $NPROCS –host $HOSTS $cmd > mpising/output.log
# eval $cmd > mpising/output.log
echo Commandline: $cmd $HOME
# eval singularity
mpirun -np $NPROCS --host $HOSTS /usr/local/bin/singularity run fmriprep-1.4.1.simg

pwd; hostname; date |tee result
echo Finished tasks