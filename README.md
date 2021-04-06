# zPerf: A Statistical Gray-box Approach to Performance Modeling and Extrapolation for Scientific Lossy Compression
----
As simulation-based scientific discovery is being further scaled up on high-performance computing systems, 
the disparity between compute and I/O has 
continued to widen. As such, domain scientists are forced to save only a small portion of their simulation data to persistent
storage, and as a consequence, important physics may be discarded for data analysis.
Error-bounded lossy compression has made tremendous progress recently in bridging the gap
between compute and I/O, and played an increasingly 
important role in science productions. Nevertheless,
a key hurdle to wide adoption of lossy compression is the lack of understanding of compression
performance, which is the result of the complex interaction between data, error bound and compression algorithm. 
In this work, we present zPerf, a statistical gray-box performance modeling approach for scientific lossy compression. Our contributions are threefold: 
1) We develop zPerf to estimate the performance of two state-of-the-art lossy compression techniques, SZ and ZFP, based on in-depth understanding and statistical modeling for data features and core compression metrics;
2) We evaluate the effectiveness of zPerf on eight real-world datasets across various domains. Based on the evaluation, we verify that zPerf model can achieve reasonable accuracy;
3) We further discuss two case studies where zPerf is applied to extrapolate the performance of SZ and ZFP with alternative encoding schemes. Through the case studies, we demonstrate the potential of zPerf for exploring the design space of lossy compression, which has hardly been studied in the literature.

- To run the compression

- To run the compression performance modeling
