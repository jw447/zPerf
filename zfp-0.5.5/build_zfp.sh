#!/bin/bash

# Build ZFP-0.5.5 on Summit@ORNL
git branch

set -e
set -x

module load cmake/3.15.2
module load cuda/10.1.168

cd build_debug
cmake -DZFP_WITH_OPENMP=ON -DZFP_WITH_CUDA=ON -DBUILD_EXAMPLES=OFF ..
make -j4
