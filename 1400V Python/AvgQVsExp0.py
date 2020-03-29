import numpy as np
from matplotlib import pyplot as plt
from matplotlib import style
import math

data = np.loadtxt("txtFiles/1400V/afterpulseQ_vs_date_Ch0.txt", unpack=True, delimiter=",")

results = np.array(data)
sorted_results = results[:, results[1, :].argsort()]

avgq = sorted_results[2]
err = sorted_results[4]
stddev = sorted_results[3]

stddev1 = stddev[:56]

stderr1 = stddev1 / (50000**0.5)


stddev2 = stddev[56:]
stderr2 = stddev2 / (200000**0.5)

err1 = np.append(stderr1,stderr2)
print(err1)

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
plt.ylim(9,11.1)
plt.title('Average afterpulse charge vs Exposure PMT Ch0')
plt.grid()
plt.savefig('SummaryPlots/1400V/AvgQVsExp0.pdf')
plt.show()
