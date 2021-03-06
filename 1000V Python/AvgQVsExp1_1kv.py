import numpy as np
from matplotlib import pyplot as plt
from matplotlib import style
import math

data = np.loadtxt("txtFiles/1000V/afterpulseQ_vs_date_Ch1_1kV.txt", unpack=True, delimiter=",")

results = np.array(data)
sorted_results = results[:, results[1, :].argsort()]

avgq = sorted_results[2]
err = sorted_results[4]

def date_converter(dateinput):
    # October
    if dateinput < 191100:
        newdate = dateinput - 191007

    # November
    elif 191100 < dateinput < 191131:
        newdate = dateinput - 191076
    # December
    elif (dateinput > 191200) and (dateinput < 191232):
        newdate = dateinput - 191146
    # January
    elif (dateinput > 200100) and (dateinput < 200132):
        newdate = dateinput - 200015
    # February
    elif (dateinput > 200200) and (dateinput < 200230):
        newdate = dateinput - 200086
    # March
    elif (dateinput > 200300) and (dateinput < 200331):
        newdate = dateinput - 200157
    return newdate


Exposure = np.array([])

for item in sorted_results[1]:
    ndates = date_converter(item)
    Exposure = np.append(Exposure,ndates)

print(sorted_results[1])
print(sorted_results[2])

plt.errorbar(Exposure,avgq, yerr=err, marker='.',capsize=2, label="title", ls = 'none')
plt.xlabel('Exposure / days since 08/10/19')
plt.ylabel('Afterpulse Charge / pC')
plt.ylim(7,8)
plt.title('Average afterpulse charge vs Exposure PMT Ch1 @ 1kV')

plt.savefig('SummaryPlots/1000V/AvgQVsExp1_1kV.pdf')
plt.show()