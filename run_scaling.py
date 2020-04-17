import numpy as np
import os

from multiarea_model import MultiAreaModel
from start_jobs import start_job
from config import submit_cmd, jobscript_template
from config import base_path
from figures.Schmidt2018_dyn.network_simulations import NEW_SIM_PARAMS


network_params, sim_params = NEW_SIM_PARAMS['Fig5'][0]

network_params['connection_params']['K_stable'] = os.path.join(
    base_path, 'figures/SchueckerSchmidt2017/K_prime_original.npy'
)

theory_params = {'dt': 0.1}

total_num_vp_per_node = 24
t_presim = 10.
t_sim = 10000.
NEST_DIR = ['/p/project/cjinb33/jinb3330/gitordner/nest-simulator/f10cd16/bin/nest_vars.sh']

# Place to store simulations
DATA_PATH =  ['/home/pronold/git_ordner/multi-area-model/datalol']

for i, nest_dir in enumerate(NEST_DIR):
    for mpi_proc_per_node in [6]:
        for num_nodes in range(16,25,8):
            for master_seed in [0, 17, 666]:
                local_num_threads = int(total_num_vp_per_node / mpi_proc_per_node)
                num_processes = (num_nodes * mpi_proc_per_node)
                data_path = DATA_PATH[i]

                sim_params.update(
                        {
                            't_presim': t_presim,
                            't_sim': t_sim,
                            'num_processes': num_processes,
                            'num_nodes': num_nodes,
                            'local_num_threads': local_num_threads,
                            'master_seed': master_seed,
                            'nest_dir': nest_dir,
                            'data_path': data_path
                            }
                        )

                if not os.path.exists(data_path):
                    os.makedirs(data_path)

                M = MultiAreaModel(network_params, simulation=True,
                                   sim_spec=sim_params,
                                   theory=True,
                                   theory_spec=theory_params)

                p, r = M.theory.integrate_siegert()

                print("Mean-field theory predicts an average "
                      "rate of {0:.3f} spikes/s across all populations.".format(np.mean(r[:, -1])))

                start_job(M.simulation.label, submit_cmd, jobscript_template, data_path)
