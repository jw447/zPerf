#!/bin/bash
  
# Build SZ-2.1.7 on Cori@NERSC
git branch

set -e

module load gcc/6.1.0
module load gsl/2.5

INSTALL_PATH=/global/cscratch1/sd/jw447/local_build/SZ/install
CC=gcc

./configure --prefix=$INSTALL_PATH --enable-openmp && make -j8 && make install
