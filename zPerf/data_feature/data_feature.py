import pandas as pd

# data length
dsize = pd.DataFrame({
    "Brown": [33554433],
    "SCALE": [70560000],
    "XGC": [42381312],
    "S3D": [1375000000],
    "CESM_ATM": [168480000],
    "NSTX_GPI_gpiData": [94555392],
    "EXAALT": [2869440],
    "Hurricane_ISABEL": [25000000],
    "HACC": [1073726487],
    "NYX": [134217728],
    "QMCPACK": [157684320]
})

# input size (byte)
isize = pd.DataFrame({
    "Brown": [268435464],
    "SCALE": [564480000],
    "XGC": [339050496],
    "S3D": [11000000000],
    "CESM_ATM": [673920000],
    "NSTX_GPI_gpiData": [378221568],
    "HACC": [4294905948],
    "NYX": [536870912],
    "QMCPACK": [630737280]
})

# data value range
drange = pd.DataFrame({
    "Brown": [1138162285.722114],
    "SCALE": [6.078464866840478e+37],
    "XGC": [1200.473323603815],
    "S3D": [15.380282525726392],
    "CESM_ATM": [7.855168951209635e-05],
    "NSTX_GPI_gpiData": [150.0],
    "EXAALT": [2017.008056640625],
    "Hurricane_ISABEL": [0.0020479534287005663],
    "HACC": [7614.87353515625],
    "NYX": [4780302.5],
    "QMCPACK": [33.01001739501953]
})
