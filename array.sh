#!/usr/bin/env bash

files=001.txt,002.txt,003.txt,004.txt
IFS=, read -a tks <<< $files
tks=($tks) # have to add this on mac.
N_ck=${#tks[@]}; echo "chunks are $N_ck"
for x in ${tks[@]}; do echo $x; done
