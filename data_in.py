#!/usr/bin/env python

# pytorch_speechMLP 
# Mirco Ravanelli 
# Montreal Institute for Learning Algoritms (MILA)
# University of Montreal 

# January 2018

# Description: 
# This code implements with pytorch a basic MLP  for speech recognition. 
# It exploits an interface to  kaldi for feature computation and decoding. 
# How to run it:
# python run_nn.py --cfg TIMIT_MLP.cfg

# data_in.py
#
# using pytorch_kaldi to get MFCC features and phone labels from ali
#
#
#

import kaldi_io
import numpy as np
import torch
from torch.autograd import Variable
import timeit
import torch.optim as optim
import os
from data_io import load_chunk,load_counts,read_conf, read_opts
import random
import torch.nn as nn
import sys


  
    
# Reading options in cfg file
options=read_conf()
print(options)

# to do options
# do_training=bool(int(options.do_training))
# do_eval=bool(int(options.do_eval))
# do_forward=bool(int(options.do_forward))

# Reading data options
fea_scp=options.fea_scp
fea_opts=options.fea_opts
lab_folder=options.lab_folder
lab_opts=options.lab_opts

out_file=options.out_file

# Reading count file from kaldi
# count_file=options.count_file
# pt_file=options.pt_file

# reading architectural options
left=int(options.cw_left)
right=int(options.cw_right)
seed=int(options.seed)
use_cuda=bool(int(options.use_cuda))
multi_gpu=bool(int(options.multi_gpu))
NN_type=options.NN_type

# reading optimization options
batch_size=int(options.batch_size)
lr=float(options.lr)
save_gpumem=int(options.save_gpumem)
opt=options.optimizer



start_time=timeit.default_timer()

# Setting torch seed
torch.manual_seed(seed)
random.seed(seed)

[data_name,data_set,data_end_index]=load_chunk(fea_scp,fea_opts,lab_folder,lab_opts,left,right,seed)
print(data_set.shape)