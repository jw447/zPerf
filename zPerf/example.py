from func import SZ_Estimation
from func import ZFP_Estimation

# dataset names
data  = ["Brown", "SCALE", "CESM_ATM", "NYX"]

# compression variables
errbound = [1e-9, 1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1]

# modeling variable
ratio = 10000 # population ratio

for i in range(0, len(data)):
    dname = data[i]
    sz_cr_e, sz_ct_e = SZ_Estimation.zperf(dname, errbound, ratio)
    zfp_cr_e, zfp_ct_e = ZFP_Estimation.zperf(dname, errbound, ratio)
