""" ZFP compression performance estimation."""
import numpy as np
import pandas as pd
import os

from func.Generate_Random_PDF import generate_rand_from_pdf
from data_feature.data_feature import dsize, drange, isize
from data_feature.zfp_Input import df_inputmean, df_emax, df_blockmean

# zfp low-level routine timings (sec)
r1 = 20.89e-9
r2 = 1.619e-8
r3 = 4.393e-9
r4 = 2.619e-8
r5 = [2.68567e-9,3.82303e-9, 3.99925e-9, 4.37074e-9]

# double precision
dname_d = ["Brown", "SCALE", "XGC", "S3D"]
# single precision
dname_f = ["CESM_ATM", "NSTX_GPI_gpiData", "NYX", "QMCPACK", "HACC"]

def zperf(dname, errbound, ratio):
    """ Compression ratio and compression throughput estimation for ZFP.
    Args:
        dname: string, name of dataset.
        errbound: list, error bound values.
        ratio: int, reciprocal of population ratio (exp. 100 means populating ratio as 1/100).
    Returns:
        cr_e: list, estimated compression ratio under given error bounds.
        ct_e: list, estimated compression throughput under given error bounds.
    """
    is_o = isize[dname].values[0]
    nelements = dsize[dname].values[0]
    nblocks = np.int(np.ceil(nelements/4))
    value_range = drange[dname].values[0]

    if dname in dname_d:
        ebits = 11
        CHAR_BIT=64
        NBMASK = 0xaaaaaaaaaaaaaaaa
    elif dname in dname_f:
        ebits = 8
        CHAR_BIT=32
        NBMASK = 0xaaaaaaaa

    # populated exponent values
    hist_emax = df_emax["{}_hist".format(dname)].values
    bins_emax = df_emax["{}_bins".format(dname)].values
    bin_midpoints = bins_emax + [np.diff(bins_emax)[0]/2] * 30
    emax_rfc = generate_rand_from_pdf(hist_emax, bin_midpoints, np.int(nblocks/ratio))

    expsize_e = []
    encode_size_e = []
    comp_time_e = []
    for err in errbound:
        ei = err * value_range
        # estimated bit plane number for each block
        max_prec_esti = emax_rfc - np.log2(ei) + 4
        # estimated zero block number
        zero_block_e = len(max_prec_esti[max_prec_esti <= 0]) * ratio
        expsize_e.append(np.int((nblocks - zero_block_e)*ebits/8))
        max_prec_e = max_prec_esti[max_prec_esti > 0]
        # Estimted value for DC component values
        hist_bm = df_blockmean["{}_hist".format(dname)].values
        bins_bm = df_blockmean["{}_bins".format(dname)].values
        bin_midpoints = bins_bm + [np.diff(bins_bm)[0]/2] * 30
        bm_rfc = generate_rand_from_pdf(hist_bm, bin_midpoints, np.int(nblocks/ratio))

        # coef mean
        coef_mean_rfc = np.array(bm_rfc)/4

        # encoding size Estimation
        encode_bits = 0
        bp_time = 0
        for (max_prec_, coef_mean_) in zip(max_prec_e, coef_mean_rfc):
            # populated coef values
            coef_rfc = np.random.laplace(loc=0.0, scale=np.absolute(coef_mean_)/2, size=4)
            coef_uint = list(map(lambda x: float((int(abs(x)) + NBMASK) ^ NBMASK), coef_rfc))
            S = np.sort(CHAR_BIT - np.log2(coef_uint))

            if S[0] >= max_prec_:
                encode_bits += 0 * int(max_prec_)
            if S[0] < max_prec_ <= S[1]:
                encode_bits += 0 * int(S[0]) + 1 * int(max_prec_ - S[0])
                bp_time += r5[0] * int(max_prec_ - S[0])
            if S[1] < max_prec_ <= S[2]:
                encode_bits += 0 * int(S[0]) + 1 * int(S[1] - S[0]) + 2 * int(max_prec_ - S[1])
                bp_time += r5[0] * int(S[1] - S[0]) + r5[1] * int(max_prec_ - S[1])
            if S[2] < max_prec_ <= S[3]:
                encode_bits += 0 * int(S[0]) + 1 * int(S[1] - S[0]) + 2 * int(S[2] - S[1]) + 3 * int(max_prec_ - S[2])
                bp_time += r5[0] * int(S[1] - S[0]) + r5[1] * int(S[2] - S[1]) + r5[2] * int(max_prec_ - S[2])
            if S[3] < max_prec_:
                encode_bits += 0 * int(S[0]) + 1 * int(S[1] - S[0]) + 2 * int(S[2] - S[1]) + 3 * int(S[3] - S[2]) + 4 * int(max_prec_ - S[3])
                bp_time += r5[0] * int(S[1] - S[0]) + r5[1] * int(S[2] - S[1]) + r5[2] * int(S[3] - S[2]) + r5[3] * int(max_prec_ - S[3])

        encode_size_e.append(encode_bits*ratio/8)
        comp_time_e.append((nblocks - zero_block_e) * (r1 + r2 + r3 + r4) + bp_time)

    cr_e = is_o/(np.array(expsize_e) + np.array(encode_size_e))
    ct_e = is_o/np.array(comp_time_e)
    return cr_e, ct_e
