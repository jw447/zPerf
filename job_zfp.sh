#!/bin/bash
#BSUB -P CSC143
#BSUB -W 01:00
#BSUB -nnodes 1
#BSUB -J zfp_performance
#BSUB -o zfp_performance.o
#BSUB -e zfp_performance.e

source ~/.bashrc
source ~/.bash_profile

# path to data directory
COMP_DATA=""

#Brown
data="Brown"
echo ${data}
rate=(1.13816229e3 1.13816229e4 1.13816229e5 1.13816229e6)
for rate_ in "${rate[@]}"; do
    echo ${rate_}
    _size=`expr $(stat -c%s $COMP_DATA/${data}.dat) / 8`
    jsrun --nrs 1 --tasks_per_rs 1 --rs_per_host 1 --gpu_per_rs 1 ${ZFP_PATH}/zfp -i ${COMP_DATA}/${data}.dat -1 $_size -d -a $rate_
done

#SCALE
data="SCALE"
echo ${data}
rate=(6.07846487e31 6.07846487e32 6.07846487e33 6.07846487e34)
for rate_ in "${rate[@]}"; do
   echo ${rate_}
   _size=`expr $(stat -c%s $COMP_DATA/${data}.dat) / 8`
   jsrun --nrs 1 --tasks_per_rs 1 --rs_per_host 1 --gpu_per_rs 1 ${ZFP_PATH}/zfp -i ${COMP_DATA}/${data}.dat -1 $_size -d -a $rate_
done

#XGC
data="XGC"
echo ${data}
rate=(1.20047332e-3 1.20047332e-2 1.20047332e-1 1.20047332e0)
for rate_ in "${rate[@]}"; do
   echo ${rate_}
   _size=`expr $(stat -c%s $COMP_DATA/${data}.dat) / 8`
   jsrun --nrs 1 --tasks_per_rs 1 --rs_per_host 1 --gpu_per_rs 1 ${ZFP_PATH}/zfp -i ${COMP_DATA}/${data}.dat -1 $_size -d -a $rate_
done

#S3D
data="S3D"
echo ${data}
rate=(1.53802825e-5 1.53802825e-4 1.53802825e-3 1.53802825e-2)
for rate_ in "${rate[@]}"; do
   echo ${rate_}
   _size=`expr $(stat -c%s $COMP_DATA/${data}.dat) / 8`
   jsrun --nrs 1 --tasks_per_rs 1 --rs_per_host 1 --gpu_per_rs 1 ${ZFP_PATH}/zfp -i ${COMP_DATA}/${data}.dat -1 $_size -d -a $rate_
done

#CESM_ATM
data="CESM_ATM"
echo ${data}
rate=(7.85516895e-11 7.85516895e-10 7.85516895e-9 7.85516895e-8)
for rate_ in "${rate[@]}"; do
   echo ${rate_}
   _size=`expr $(stat -c%s $COMP_DATA/${data}.dat) / 4`
   jsrun --nrs 1 --tasks_per_rs 1 --rs_per_host 1 --gpu_per_rs 1 ${ZFP_PATH}/zfp -i ${COMP_DATA}/${data}.dat -1 $_size -f -a $rate_
done

#nst
data="NSTX_GPI_gpiData"
echo ${data}
rate=(1.5e-4 1.5e-3 1.5e-2 1.5e-1)
for rate_ in "${rate[@]}"; do
   echo ${rate_}
   _size=`expr $(stat -c%s $COMP_DATA/${data}.dat) / 4`
   jsrun --nrs 1 --tasks_per_rs 1 --rs_per_host 1 --gpu_per_rs 1 ${ZFP_PATH}/zfp -i ${COMP_DATA}/${data}.dat -1 $_size -f -a $rate_
done

#HACC
data="HACC"
echo ${data}
rate=(7.61487354e-3 7.61487354e-2 7.61487354e-1 7.61487354e0)
for rate_ in "${rate[@]}"; do
   echo ${rate_}
   _size=`expr $(stat -c%s $COMP_DATA/${data}.dat) / 4`
   jsrun --nrs 1 --tasks_per_rs 1 --rs_per_host 1 --gpu_per_rs 1 ${ZFP_PATH}/zfp -i ${COMP_DATA}/${data}.dat -1 $_size -f -a $rate_
done

#NYX
data="NYX"
echo ${data}
rate=(4.7803025e0 4.7803025e1 4.7803025e2 4.7803025e3)
for rate_ in "${rate[@]}"; do
   echo ${rate_}
   _size=`expr $(stat -c%s $COMP_DATA/${data}.dat) / 4`
   jsrun --nrs 1 --tasks_per_rs 1 --rs_per_host 1 --gpu_per_rs 1 ${ZFP_PATH}/zfp -i ${COMP_DATA}/${data}.dat -1 $_size -f -a $rate_
done
