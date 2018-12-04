#!/usr/bin/env bash

function run_py {
  python run_nn_multilabel.py --cfg exp/bell_mp/ck_$1.cfg
}
export -f run_py
# using parallel
parallel --verbose -j 2 run_py {} ::: $(seq 0 63)