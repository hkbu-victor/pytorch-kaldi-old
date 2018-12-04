#!/usr/bin/env bash

##########################################################
# pytorch_speechMLP                                      
# Mirco Ravanelli 
# Montreal Institute for Learning Algoritms (MILA)
# University of Montreal
# Feb 2018
#
# generate cfg files for Bell_MP data set
# - eval + forward
# -
#
#
#
#
##########################################################

           
function write_conf {
    # Writing the single-iteration config file
    echo "[todo]" > $conf_file
    echo "do_training=$do_training" >> $conf_file
    echo "do_eval=$do_eval" >> $conf_file
    echo "do_forward=$do_forward" >> $conf_file
    echo " " >> $conf_file
    
    echo "[data]" >> $conf_file
    echo "fea_scp=$fea_chunk" >> $conf_file
    echo "fea_opts=$fea_opts" >> $conf_file
    echo "lab_folder=$lab_folder" >> $conf_file
    echo "lab_opts=$lab_opts" >> $conf_file
    echo "pt_file=$pt_file" >> $conf_file
    echo "count_file=$count_file" >> $conf_file
    echo "out_file=$out_file" >> $conf_file
    echo " " >> $conf_file
    
    echo "[architecture]" >> $conf_file
    echo "NN_type=$NN_type" >> $conf_file
    echo "cnn_pre=$cnn_pre" >> $conf_file
    echo "hidden_dim=$hidden_dim" >> $conf_file
    echo "N_hid=$N_hid" >> $conf_file
    echo "drop_rate=$drop_rate" >> $conf_file
    echo "use_batchnorm=$use_batchnorm" >> $conf_file
    echo "use_laynorm=$use_laynorm" >> $conf_file
    echo "cw_left=$cw_left" >> $conf_file
    echo "cw_right=$cw_right" >> $conf_file
    echo "seed=$seed" >> $conf_file
    echo "use_cuda=$use_cuda" >> $conf_file
    echo "bidir=$bidir" >> $conf_file
    echo "resnet=$resnet" >> $conf_file
    echo "skip_conn=$skip_conn" >> $conf_file
    echo "act=$act" >> $conf_file
    echo "act_gate=$act_gate" >> $conf_file
    echo "resgate=$resgate" >> $conf_file
    echo "minimal_gru=$minimal_gru" >> $conf_file
    echo "cost=$cost" >> $conf_file
    echo "twin_reg=$twin_reg" >> $conf_file
    echo "twin_w=$twin_w" >> $conf_file
    echo "multi_gpu=$multi_gpu" >> $conf_file
    echo " " >> $conf_file
    
    echo "[optimization]" >> $conf_file
    echo "lr=$lr" >> $conf_file
    echo "optimizer=$optimizer" >> $conf_file
    echo "batch_size=$batch_size" >> $conf_file
    echo "save_gpumem=$save_gpumem" >> $conf_file
}

# Reading Param File
cfg_file=$1
cmd=""

# Parsing cfg file
if [[ $(uname -s) == Darwin ]]
then
    source $cfg_file
else
    source <(grep = $cfg_file)
fi

# source $cfg_file
IFS=, read -a te_fea_scp_list <<< $te_fea_scp

# creating output folder
mkdir -p $out_folder

if [[ $(uname -s) == Darwin ]]
then
    te_fea_scp_list=($te_fea_scp_list)
fi

# Number of test chunks
N_ck=${#te_fea_scp_list[@]}; echo "chunks are $N_ck"

sleep_time=3

for chunk in $(seq  0 "$(($N_ck-1))"); do

    fea_chunk=${te_fea_scp_list[$chunk]}
    fea_opts=$te_fea_opts
    lab_folder=$te_lab_folder
    lab_opts=$te_lab_opts

    out_file=$out_folder"/ck_"$chunk".pkl"
    info_file=$out_folder"/ck_"$chunk".info"
    conf_file=$out_folder"/ck_"$chunk".cfg"

    [ -e $conf_file ] && rm $conf_file

    do_training=0
    do_eval=1
    do_forward=1

    # writing config file
    write_conf

#    # single-chunk
#    if [ ! -f "$info_file" ]; then
#     $cmd python run_nn_multilabel.py --cfg $conf_file 2> $out_folder/log.log || exit 1
#    fi
#
#    while [ ! -f $info_file ]; do
#     sleep $sleep_time
#    done

done

#function run_py {
#  python run_nn_multilabel.py --cfg exp/bell_mp/ck_$1.cfg
#}
## using parallel
#export -f run_py
#parallel -j 2 --tmux --fg run_py {} ::: 0 1
