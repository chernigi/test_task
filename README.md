SAX.py implements the dimentionality reduction technique SAX for the time series TS. TS is represented by the sin function with noise added.

SAX consists out of 3 steps:
# 1. Normalization
TS values are normalized using (ts-mean)/standard_deviation, so that the normalized TS has a mean of 0 and standard deviation of 1.
# 2. PAA representation
first the normalized TS is divided on n_chunks equal parts and for every chunk the mean is calculated
# 3. PAA is transformed to SAX
Using the selected alphabet and a set of breakpoints (calculated using numpy.stats), each value of PAA-representation is encoded as a alphabet character.
