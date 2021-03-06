# zPerf: A Statistical Gray-box Approach to Performance Modeling and Extrapolation for Scientific Lossy Compression

As simulation-based scientific discovery is being further scaled up on high-performance computing systems, the disparity between compute and I/O has continued to widen. As such, domain scientists are forced to save only a small portion of their simulation data to persistent storage, and as a consequence, important physics may be discarded for data analysis. Error-bounded lossy compression has made tremendous progress recently in bridging the gap between compute and I/O, and played an increasingly important role in science productions. Nevertheless, a key hurdle to the wide adoption of lossy compression is the lack of understanding of compression performance, which is the result of the complex interaction between data, error bound, and compression algorithm. In this work, we present zPerf, a statistical gray-box performance modeling approach for scientific lossy compression. Our contributions are threefold: 1) We develop zPerf to estimate the performance of two state-of-the-art lossy compression techniques, SZ and ZFP, based on in-depth understanding and statistical modeling for data features and core compression metrics; 2) We evaluate the effectiveness of zPerf on eight real-world datasets across various domains. Based on the evaluation, we verify that zPerf model can achieve reasonable accuracy; 3) We further discuss two case studies where zPerf is applied to extrapolate the performance of SZ and ZFP with alternative encoding schemes. Through the case studies, we demonstrate the potential of zPerf for exploring the design space of lossy compression, which has hardly been studied in the literature.

## Compression softwares

We use SZ-2.1.7.0 and ZFP-0.5.5 in this work. The source code of SZ and ZFP are forked from https://github.com/szcompressor/SZ and https://github.com/LLNL/zfp respectively. For SZ and ZFP, we include the build commands for installation, named as *build_sz.sh* and *build_zfp.sh* in each compressor folder.

## To run the compression

We provide the example job scripts of running SZ on Cori, named as *job_sz.sh,* and running ZFP on Summit, named as *job_zfp.sh*. Users need to specify the installation path of each compressor and the data directory in the job scripts.

For SZ, we set the number of quantization intervals as 65536 and SZ_Mode as SZ_BEST_SPEED, where the lossless backend is not performed. We set the errBoundMode as REL (relative error bound) and the relative error ratio as [1E-6, 1E-5, 1E-4, 1E-3]. For ZFP, we adopt fixed_accuracy mode and set the absolute error bound as the production of relative error ratio and data range. The relative error ratio for ZFP is set to [1E-6, 1E-5, 1E-4, 1E-3] as well.

## To run the compression performance modeling

### Requirements

The following python packages are used in zPerf and can be installed by 

```python
python3 -r requirements.txt
```

- numpy 1.19.5
- pandas 1.1.5
- huffman 0.1.2

### Running the performance modeling

The implementation of our work is located at zPerf. The input to the performance modeling is located at data_feature. In this folder, ```data_feature.py``` contains the general descriptions of the input dataset, for example data length, data size, and value range. ```sz_input.py``` and ```zfp_input.py``` contain the features for SZ, and ZFP modeling respectively. We include the features of datasets used in the work. For other datasets, uses need to obtain them prior to running the performance modeling.

The modeling functions are defined in func. 
Both in ```SZ_Estimation.py``` and ```ZFP_Estimation.py```, the function ```zperf(dname, errorbound, ratio)```is defined to estimate the compression ratio and compression throughput for SZ and ZFP. The function takes three parameters: the dataset name ```dname```, error bound values ```errorbound```, and population ratio ```ratio```. The return values are the estimated compression ratio and compression throughput.

We demonstrate an example of running compression performance modeling in ```example.py```. Users can try the example by running

```python
python3 example.py
```
