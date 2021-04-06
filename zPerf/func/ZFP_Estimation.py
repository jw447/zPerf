""" ZFP compression performance estimation."""
import numpy as np
import pandas as pd
import os

from data_feature.data_feature import dsize, drange, isize
from data_feature.zfp_InputMean import df_inputmean
from func.Generate_Random_PDF import generate_rand_from_pdf

# double precision
dname_d = ["Brown", "SCALE", "XGC", "S3D"]
# single precision
dname_f = ["CESM_ATM", "NSTX_GPI_gpiData", "NYX", "QMCPACK", "HACC"]

def zero_block_esti(dname, errbound, ratio):
    if dname in dname_d:
        ebits = 11
        CHAR_BIT=64
        NBMASK = 0xaaaaaaaaaaaaaaaa
    elif dname in dname_f:
        ebits = 8
        CHAR_BIT=32
        NBMASK = 0xaaaaaaaa

    nblocks = np.int(np.ceil(dsize[dname].values[0]/4))

    # populated emax values
    hist_emax = zfp_Emax.df_emax["{}_hist".format(dname)].values
    bins_emax = zfp_Emax.df_emax["{}_bins".format(dname)].values
    bin_midpoints = bins_emax + [np.diff(bins_emax)[0]/2] * 30
    emax_rfc = generate_rand_from_pdf(hist_emax, bin_midpoints, np.int(nblocks/ratio))

    zero_block_e = []
    for err in errbound:
        ei = err * drange[dname].values[0]
        # estimated max_prec
        max_prec_esti = emax_rfc - np.log2(ei) + 4
        zero_block_e.append(len(max_prec_esti[max_prec_esti <= 0])*ratio)

    return zero_block_e

def exp_size_esti(dname, errbound, ratio):
    if dname in dname_d:
        ebits = 11
        CHAR_BIT=64
        NBMASK = 0xaaaaaaaaaaaaaaaa
    elif dname in dname_f:
        ebits = 8
        CHAR_BIT=32
        NBMASK = 0xaaaaaaaa

    nblocks = np.int(np.ceil(dsize[dname].values[0]/4))
    zblocks = zero_block_esti(dname, errbound, ratio)
    return (nblocks-np.array(zblocks))*ebits/8/1024/1024

def encode_size_esti(dname, errbound, ratio):
    if dname in dname_d:
        ebits = 11
        CHAR_BIT=64
        NBMASK = 0xaaaaaaaaaaaaaaaa
    elif dname in dname_f:
        ebits = 8
        CHAR_BIT=32
        NBMASK = 0xaaaaaaaa

    nblocks = np.int(np.ceil(dsize[dname].values[0]/4))

    # populated emax values
    hist_emax = zfp_Emax.df_emax["{}_hist".format(dname)].values
    bins_emax = zfp_Emax.df_emax["{}_bins".format(dname)].values
    bin_midpoints = bins_emax + [np.diff(bins_emax)[0]/2] * 30
    emax_rfc = generate_rand_from_pdf(hist_emax, bin_midpoints, np.int(nblocks/ratio))

    encode_size_e = []
    for err in errbound:
        ei = err * drange[dname].values[0]
        # estimated max_prec
        max_prec_e = emax_rfc - np.log2(ei) + 4
        zblocks_e  = len(max_prec_e[max_prec_e <= 0])
        max_prec_e = max_prec_e[max_prec_e > 0] # for those poositive ones

        # populated coef_mean
        hist_coefmean = zfp_CoefMean.df_coefmean["{}_hist".format(dname)].values
        bins_coefmean = zfp_CoefMean.df_coefmean["{}_bins".format(dname)].values
        bin_midpoints = bins_coefmean + [np.diff(bins_coefmean)[0]/2] * 30
        coef_mean_rfc = generate_rand_from_pdf(hist_coefmean, bin_midpoints, len(max_prec_e))

        encode_bits = []
        for (max_prec_, coef_mean_) in zip(max_prec_e, coef_mean_rfc):
            # populated coef values
            coef_rfc = np.random.laplace(loc=0.0, scale=coef_mean_/2, size=4)
            coef_uint = list(map(lambda x: (np.int(np.absolute(x)) + NBMASK) ^ NBMASK, coef_rfc))
            coef_uint = np.array(coef_uint, dtype=np.float)

            S = np.sort(CHAR_BIT - np.ceil(np.log2(coef_uint)))

            if S[0] >= max_prec_:
                for _ in np.arange(np.int(max_prec_)):
                    encode_bits.append(0)
            elif S[0]< max_prec_:
                if S[1] >= max_prec_:
                    for _ in np.arange(np.int(S[0])):
                        encode_bits.append(0)
                    for _ in np.arange(np.int(max_prec_ - S[0])):
                        encode_bits.append(1)
                elif S[1] < max_prec_:
                    if S[2] >= max_prec_:
                        for _ in np.arange(np.int(S[0])):
                            encode_bits.append(0)
                        for _ in np.arange(np.int(S[1] - S[0])):
                            encode_bits.append(1)
                        for _ in np.arange(np.int(max_prec_-S[1])):
                            encode_bits.append(2)
                    elif S[2] < max_prec_:
                        if S[3] >= max_prec_:
                            for _ in np.arange(np.int(S[0])):
                                encode_bits.append(0)
                            for _ in np.arange(np.int(S[1] - S[0])):
                                encode_bits.append(1)
                            for _ in np.arange(np.int(S[2] - S[1])):
                                encode_bits.append(2)
                            for _ in np.arange(np.int(max_prec_ - S[2])):
                                encode_bits.append(3)
                        elif S[3] < max_prec_:
                            for _ in np.arange(np.int(S[0])):
                                encode_bits.append(0)
                            for _ in np.arange(np.int(S[1] - S[0])):
                                encode_bits.append(1)
                            for _ in np.arange(np.int(S[2] - S[1])):
                                encode_bits.append(2)
                            for _ in np.arange(np.int(S[3] - S[2])):
                                encode_bits.append(3)
                            for _ in np.arange(np.int(max_prec_ - S[3])):
                                encode_bits.append(4)

        encode_size_e.append(np.sum(encode_bits)*ratio/8/1024/1024)

    return encode_size_e

def zperf(dname, errbound, ratio):
    is_o = isize[dname].values[0]/1024/1024
    if dname in dname_d:
        ebits = 11
        CHAR_BIT=64
        NBMASK = 0xaaaaaaaaaaaaaaaa
    elif dname in dname_f:
        ebits = 8
        CHAR_BIT=32
        NBMASK = 0xaaaaaaaa

    nblocks = np.int(np.ceil(dsize[dname].values[0]/4))
    exp_size_e = exp_size_esti(dname, errbound, ratio)

    # populated emax values
    hist_emax = zfp_Emax.df_emax["{}_hist".format(dname)].values
    bins_emax = zfp_Emax.df_emax["{}_bins".format(dname)].values
    bin_midpoints = bins_emax + [np.diff(bins_emax)[0]/2] * 30
    emax_rfc = generate_rand_from_pdf(hist_emax, bin_midpoints, np.int(nblocks/ratio))

    Num_zero_blocks = []
    Num_max_prec = []
    encode_size_e = []
    for err in errbound:
        ei = err * drange[dname].values[0]
        # estimated max_prec
        max_prec_e = emax_rfc - np.log2(ei) + 4
        zblocks_e  = len(max_prec_e[max_prec_e <= 0])
        max_prec_e = max_prec_e[max_prec_e > 0] # for those poositive ones
        Num_zero_blocks.append(zblocks_e*ratio)
        Num_max_prec.append(np.sum(max_prec_e)*ratio)

        # populated coef_mean
        hist_coefmean = zfp_CoefMean.df_coefmean["{}_hist".format(dname)].values
        bins_coefmean = zfp_CoefMean.df_coefmean["{}_bins".format(dname)].values
        bin_midpoints = bins_coefmean + [np.diff(bins_coefmean)[0]/2] * 30
        coef_mean_rfc = generate_rand_from_pdf(hist_coefmean, bin_midpoints, len(max_prec_e))

        encode_bits = 0
        bp_time = 0
        for (max_prec_, coef_mean_) in zip(max_prec_e, coef_mean_rfc):
            # populated coef values
            coef_rfc = np.random.laplace(loc=0.0, scale=coef_mean_/2, size=4)
            coef_uint = list(map(lambda x: float((int(abs(x)) + NBMASK) ^ NBMASK), coef_rfc))
            S = np.sort(CHAR_BIT - np.log2(coef_uint))
            if S[0] >= max_prec_:
                encode_bits += 0 * int(max_prec_)
            if S[0] < max_prec_ <= S[1]:
                encode_bits += 0 * int(S[0]) + 1 * int(max_prec_ - S[0])
                bp_time += 2.68567 * int(max_prec_ - S[0])
            if S[1] < max_prec_ <= S[2]:
                encode_bits += 0 * int(S[0]) + 1 * int(S[1] - S[0]) + 2 * int(max_prec_ - S[1])
                bp_time += 2.68567 * int(S[1] - S[0]) + 3.82303 * int(max_prec_ - S[1])
            if S[2] < max_prec_ <= S[3]:
                encode_bits += 0 * int(S[0]) + 1 * int(S[1] - S[0]) + 2 * int(S[2] - S[1]) + 3 * int(max_prec_ - S[2])
                bp_time += 2.68567 * int(S[1] - S[0]) + 3.82303 * int(S[2] - S[1]) + 3.99925 * int(max_prec_ - S[2])
            if S[3] < max_prec_:
                encode_bits += 0 * int(S[0]) + 1 * int(S[1] - S[0]) + 2 * int(S[2] - S[1]) + 3 * int(S[3] - S[2]) + 4 * int(max_prec_ - S[3])
                bp_time += 2.68567 * int(S[1] - S[0]) + 3.82303 * int(S[2] - S[1]) + 3.99925 * int(S[3] - S[2]) + 4.37074 * int(max_prec_ - S[3])

        encode_size_e.append(encode_bits*ratio/8/1024/1024)

    # comp_time = (nblocks - np.array(Num_zero_blocks)) * (2.089e-9 + 1.619e-08 + 4.393e-09 + 2.619e-08) + np.array(Num_max_prec) * 7.023e-09
    comp_time = (nblocks - np.array(Num_zero_blocks)) * (20.89e-9 + 1.619e-08 + 4.393e-09 + 2.619e-08) + bp_time/1e9

    cr_e = is_o/(exp_size_e + encode_size_e)
    ct_e = is_o/comp_time
    return cr_e, ct_e
