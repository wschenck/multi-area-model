# This bash script gives a rough feeling of the overall rate of the network
# This is achieved by counting all spikes that were emitted via counting the lines of the gdf files
# The rate is the number of spikes divided by time divided by the total number of neurons
# The rate should roughly be somewehere between 10 and 16 Hz
# Note: this probably will not be too accurate with NEST 3 due to the way the spikes are written out. But this has to be checked.
# Run this script by providing the correct path to the simulated data, i.e. change data_dir
# Also: This might take some time, couple of hours? I guess it would be best to run the script inside of a tmux session such that one can disconnect the ssh session and attach to it later when reconnecting.

data_dir=XXX
index=0
total_spikes=0
total_num_neurons=0
echo tasks,num_nodes,dir,num_neurons,total_time_seconds,spikes,rate > rates.txt
for dir in ${data_dir}/*/recordings
do
    params_file=$(ls ${dir}/../custom_params_*)
     echo $params_file

    spikes=$(cat ${dir}/*.gdf | wc -l)

    tasks=$(python -c "import json; fn = open('${params_file}'); tmp=json.load(fn); print(tmp['sim_params']['num_processes']); fn.close()")
    num_nodes=$(python -c "import json; fn = open('${params_file}'); tmp=json.load(fn); print(tmp['sim_params']['num_nodes']); fn.close()")
    tsim=$(python -c "import json; fn = open('${params_file}'); tmp=json.load(fn); print(tmp['sim_params']['t_sim']); fn.close()")
    tpresim=10. #$(python -c "import json; fn = open('${params_file}'); tmp=json.load(fn); print(tmp['sim_params']['t_presim']); fn.close()")
    total_time_seconds=$(python -c "print((${tsim} + ${tpresim})/ 1000.)")
    num_neurons=$(grep -e "Number of local nodes:" -rw ${dir}/../*.o | awk '{sum += $5} END {print sum/2.}')

    rate=$(python -c  "print(${spikes} / ${total_time_seconds} / ${num_neurons})")

    echo ${tasks},${num_nodes},${dir},${num_neurons},${total_time_seconds},${spikes},${rate} >> rates.txt

    index=$((${index}+1))
    total_spikes=$((${total_spikes}+${spikes}))
    total_num_neurons=$((${total_num_neurons}+${num_neurons}))
done

mean_rate=$(python -c "print(${total_spikes} / ${total_time_seconds} / ${total_num_neurons})")
echo There were ${index} runs
echo There were ${total_spikes} spikes in total
echo The mean rate is ${mean_rate}
