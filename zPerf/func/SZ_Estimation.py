""" SZ compression performance estimation."""
import numpy as np
import pandas as pd
import os
import huffman

from func.Generate_Random_PDF import generate_rand_from_pdf
from data_feature.data_feature import dsize, isize, drange
from data_feature.sz_Input import abschg_var, df_abschg, qf_var

# sz compression configurations
qf = 65536

# sz low-level routine timings (sec)
r1 = 3.26e-8
r2 = 2.89e-7
r3 = 4.46e-9
r4 = 4.91e-9
r5 = 5.76e-9
r6 = 4.58e-9

def treeSize_esti(nodecount):
    """ Huffman tree structure size estimation.
    Arg:
        nodecount: integer, number of tree nodes.
    Return:
        treeSize : integer, Huffman tree structure size (byte).
    """
    if nodecount < 256:
        treeSize = 7*nodecount+1
    elif nodecount <= nodecount < 65536:
        treeSize = 9*nodecount+1
    elif nodecount >= 65536:
        treeSize = 13*nodecount+1
    return treeSize

def zperf(dname, errbound, ratio):
    """ Compression ratio and compression throughput estimation for SZ.

    # low-level metrics
    hr_e: estimated curve-fitting efficiency.
    nc_e: estimated number of Huffman tree nodes.
    # high-level metrics
    ts_e: estimated Huffman tree structure size.
    es_e: estimated Huffman encoding size.
    cht_e: estimated curve-fitting and quantization time.
    cmt_e: estimated curve-missed data encoding time.
    tc_e: estimated tree construction time.
    ec_e: estimated encoding time.

    Args:
        dname: string, name of dataset.
        errbound: list, error bound values.
        ratio: int, reciprocal of population ratio (exp. 100 means populating ratio as 1/100).
    Returns:
        cr_e: list, estimated compression ratio under given error bounds.
        ct_e: list, estimated compression throughput (bytes/sec) under given error bounds.
    """
    is_o = isize[dname].values[0]
    nelements = dsize[dname].values[0]
    value_range = drange[dname].values[0]
    hr_e = []
    cht_e = []
    cmt_e = []
    # curve-fitting efficiency estimation
    abschg_hist = df_abschg[dname+"_hist"].values
    for j in range(0, len(errbound)):
        curve_hit_j = 0
        for k in range(j, 19 - j):
            curve_hit_j += abschg_hist[k]
        hr_e.append(curve_hit_j/nelements)
        curve_miss_j = nelements - curve_hit_j
        cht_e_ = r1 * curve_hit_j
        cmt_e_ = r2 * curve_miss_j
        cht_e.append(cht_e_)
        cmt_e.append(cmt_e_)
    hr_e = np.flip(hr_e)

    # curve-fitting and quantization time
    cht_e = np.flip(cht_e)
    # curve-missed data encoding time
    cmt_e = np.flip(cmt_e)

    cr_e = []
    ct_e = []
    for j in range(0, len(errbound)):
        qf_var_ = qf_var[dname].values[j]
        qf_rfc = np.random.normal(qf/2, np.sqrt(qf_var_), np.int(nelements/ratio))
        qf_rfc = np.array(qf_rfc, dtype=np.int64)
        qf_rfc = np.append(qf_rfc, [0, 0])
        nv_e = len(np.unique(qf_rfc))
        nc_e = 2 * nv_e - 1
        ts_e = treeSize_esti(nc_e)

        hist_qf, bins_qf = np.histogram(qf_rfc, bins=np.arange(0, qf+2, 1))
        code = []
        for h, b in zip(hist_qf, bins_qf[:-1]):
            if h > 0:
                code.append(("{}".format(b), h))
        code_book = huffman.codebook(code)

        es_e = 0
        for h, b in zip(hist_qf, bins_qf[:-1]):
            if h > 0:
                es_e += (h*len(code_book["{}".format(b)])*ratio)/8

        tc_e = r3 * nelements + nc_e * (r4+r5)
        ec_e = r6 * nelements
        cr_e.append(is_o/(ts_e + es_e))
        ct_e.append(is_o/(cht_e[j] + cmt_e[j] + tc_e + ec_e))

    return cr_e, ct_e
