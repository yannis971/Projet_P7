import time
from dask import dataframe as dd
START_TIME = time.time()
dask_df = dd.read_csv('dataset1_P7.csv')
END_TIME = time.time()
print("Read csv with dask: ", (END_TIME-START_TIME), "sec")