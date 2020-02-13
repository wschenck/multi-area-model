# Absolut path of repository
base_path = '/p/project/cjinb33/jinb3330/gitordner/mam_benchmarking/2_14/multi-area-model'

# Place to store simulations
data_path = '/p/scratch/cjinb33/jinb3330/mam_benches/2_14/fig5_params_kernel_status'

# Template for jobscripts
jobscript_template = """#!/bin/bash -x
#SBATCH --job-name MAM_4g
#SBATCH -o {sim_dir}/{label}.%j.o
#SBATCH -e {sim_dir}/{label}.%j.e
#SBATCH --mem=120G
#SBATCH --time=00:45:00
#SBATCH --exclusive
#SBATCH --cpus-per-task={local_num_threads}
#SBATCH --ntasks={num_processes}
#SBATCH --nodes={num_nodes}
#SBATCH --mail-type=END,FAIL # notifications for job done & fail
#SBATCH --mail-user=j.pronold@fz-juelich.de
#SBATCH --account jinb33

module purge
module use /usr/local/software/jureca/OtherStages
module load Stages/2018b
module load GCC CMake ParaStationMPI Python SciPy-Stack GSL
# source /p/project/cjinb33/jinb3330/gitordner/nest-simulator/7f0ccca/bin/nest_vars.sh # NEST 2.18 with timer
# source /p/project/cjinb33/jinb3330/gitordner/nest-simulator/d7aa792/bin/nest_vars.sh # NEST 2.14 with timer
source /p/project/cjinb33/jinb3330/gitordner/nest-simulator/f10cd16/bin/nest_vars.sh # NEST 2.14 with timer

export KMP_AFFINITY=scatter,verbose
export LD_PRELOAD=/p/project/cjinb33/jinb3330/jemalloc/lib/libjemalloc.so

srun python -u {base_path}/run_simulation.py {label} {network_label}"""

# Command to submit jobs on the local cluster
submit_cmd = 'sbatch' 
