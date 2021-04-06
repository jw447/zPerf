""" SZ compression performance estimation."""
import numpy as np
import pandas as pd
import os

from data_feature.data_feature import dsize, isize
from data_feature.sz_Input import abschg_var, df_abschg

def treeSize_esti(nodecount):
    """
    Huffman tree structure size estimation.
    INPUT:
    nodecount: integer, number of tree nodes
    RETURN:
    treeSize : integer, Huffman tree structure size (byte)
    """
    if nodecount < 256:
        treeSize = 7*nodecount+1
    elif nodecount <= nodecount < 65536:
        treeSize = 9*nodecount+1
    elif nodecount >= 65536:
        treeSize = 13*nodecount+1
    return treeSize

def encodeSize_esti(dname, err, ratio):
    """

    """
    qf = 65536
    nelements = dsize[dname].values[0]
    df = pd.read_csv(os.path.join(dpath_sz_bitlen, "{}_{}_{}_tree_s{}.csv".format(dname, err, qf, ratio)))
    states = df.state.values
    nc_e = len(np.unique(states)) * 2 - 1
    bits  = df.bit.values
    hists, bins = np.histogram(bits, bins=range(min(bits), max(bits)+2))
    es_e = 0
    for h_, b_ in zip(hists, bins[:-1]):
        es_e += (h_*b_*ratio)/8
    return nc_e, es_e

def outlierSize_esti(dname):
    """
    Curve_missed data points size
    INPUT:
    RETURN:
    """
    ByteLen = reqLen / 8
    BitLen  = reqLen % 8
    miss_count = np.int((1 - hit_ratio) * nelements)

    bitsize  = np.ceil(BitLen * miss_count / 8)
    leadsize = np.ceil(2 * miss_count / 8)
    bytesize = np.ceil((ByteLen - 1.5) * miss_count)
    return (bytesize + bitsize + leadsize)

def zperf(dname, errbound, ratio):
    """
    INPUT:
    dname:    string, name of the dataset
    errbound: list,   the error bound values
    ratio:    int,    the reciprocal of population ratio (100 means populating ratio as 1/100)
    RETURN:
    cr_e:     list,   estimated compression ratio
    ct_e:     list,   estimated compression throughput
    # low-level metrics
    hr_e_:    list,   estimated hit ratio
    nc_e_:    list,   estimated node_count
    # high-level metrics
    es_e_:    list,   estimated Huffman encoding size
    ts_e_:    list,   estimated Huffman tree structure size
    cht_e:    list,   curve-fit cost
    cmt_e:    list,   curve-missed cost
    tc_e:     list,   treecost
    ec_e:     list,   encodecost

    """
    nelement = dsize[dname].values[0]
    is_o = isize[dname].values[0]
    hr_e = []
    cr_e = []
    ct_e = []
    cht_e = []
    cmt_e = []
    abschg_hist = df_abschg[dname+"_hist"].values
    for j in range(0, len(errbound)):
        curve_hit_j = 0
        for k in range(j, 19 - j):
            curve_hit_j += abschg_hist[k]
        hr_e.append(curve_hit_j/nelement)
        curve_miss_j = nelement - curve_hit_j
        cht_e_ = 3.263170580329312e-08 * curve_hit_j
        cmt_e_ = 2.895183555652347e-07*curve_miss_j
        cht_e.append(cht_e_)
        cmt_e.append(cmt_e_)
    hr_e = np.flip(hr_e)
    cht_e = np.flip(cht_e)
    cmt_e = np.flip(cmt_e)

    for j in range(0, len(errbound)):
        # nhit = np.int(nelement*hr_e[j]/ratio)
        # qf_var_ = qf_var[dname].values[j]
        # output components
        nc_e_ , es_e_ = encodesize_esti(dname, errbound[j], ratio)
        ts_e_ = treeSize_esti(nc_e_)
        os_e_ = outlierSize_esti(dname)[j]
        # print(os_e_)
        cr_e.append(is_o/(ts_e_ + es_e_ + os_e_))
        # time components
        tree1_e = 0.0007
        tree2_e = 3.811e-07 * nc_e_
        tree3_e = 4.460e-09 * nelement
        tree4_e = 4.9e-8 * (nc_e_*np.log2(nc_e_))
        tree5_e = 1.0876e-6 * nc_e_
        tc_e_ = tree1_e + tree2_e + tree3_e + tree4_e + tree5_e
        ec_e_ = 2.758e-8 * nelement
        ct_e.append(is_o/(cht_e[j] + cmt_e[j] + tc_e_ + ec_e_))

    return cr_e, ct_e
