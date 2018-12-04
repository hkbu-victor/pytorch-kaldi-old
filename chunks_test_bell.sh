#!/usr/bin/env bash

# chunk size will be roughly 5K words
./create_chunks.sh $KALDI_ROOT/egs/timit/s5/data/test_bell mfcc_shu 64 test_bell 0
