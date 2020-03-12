import numpy as np
from matplotlib import pyplot as plt
from matplotlib import style
import math

data = np.loadtxt("txtFiles/1000V/apulseNUM_vs_date_Ch0_1kV.txt", unpack=True, delimiter=",")
results = np.array(data)

sorted_results = results[:, results[2, :].argsort()]

print(sorted_results[2])