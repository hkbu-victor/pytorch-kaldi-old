#!/usr/bin/env bash

alidir=$KALDI_ROOT/egs/timit/s5/exp/tri3_ali

num_pdf=$(hmm-info $alidir/final.mdl | awk '/pdfs/{print $4}')
labels_tr_pdf="ark:ali-to-pdf $alidir/final.mdl \"ark:gunzip -c $alidir/ali.*.gz |\" ark:- |"
analyze-counts --verbose=1 --binary=false --counts-dim=$num_pdf "$labels_tr_pdf" ${alidir}/ali_train_pdf.counts
