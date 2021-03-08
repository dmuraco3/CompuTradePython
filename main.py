from numba import cuda
import numpy as np
print(cuda.gpus)

@cuda.jit
def matmul():
    for i in range(100000):
