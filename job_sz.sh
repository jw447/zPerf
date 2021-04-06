#!/bin/sh
#SBATCH -q debug
#SBATCH -N 1
#SBATCH -t 00:30:00
#SBATCH -C knl
#SBATCH -J sz_performance
#SBATCH -e sz_performance.e
#SBATCH -o sz_performance.o

date
source ~/.bashrc
source ~/.bash_profile

# path to data directory
LARGEDATA_PATH=""

# relative error bounds
rate=(1E-9 1E-8 1E-7 1E-6 1E-5 1E-4 1E-3 1E-2 1E-1)

# double data
dataName_d=("Brown" "SCALE" "XGC" "S3D")
# float data
dataName_f=("CESM_ATM" "NSTX_GPI_gpiData" "NYX" "HACC")

for data in "${dataName_d[@]}"; do
for rate_ in "${rate[@]}"; do
  echo "data: $data, rate: $rate_"
  _size=`expr $(stat -c%s $LARGEDATA_PATH/${data}.dat) / 8`
  srun -n1 -c 272 ${SZ_PATH}/sz -z -d -c sz.config -M REL -R $rate_ -i ${LARGEDATA_PATH}/${data}.dat -1 $_size

done
done

for data in "${dataName_f[@]}"; do
for rate_ in "${rate[@]}"; do
  echo "data: $data, rate: $rate_"
  _size=`expr $(stat -c%s $LARGEDATA_PATH/${data}.dat) / 4`
  srun -n1 -c 272 ${SZ_PATH}/sz -z -f -c sz.config -M REL -R $rate_ -i ${LARGEDATA_PATH}/${data}.dat -1 $_size
done
done
