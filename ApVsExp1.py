import numpy as np
from matplotlib import pyplot as plt
from matplotlib import style
import math

data = np.loadtxt("txtFiles/1400V/apulseNUM_vs_date_Ch1_batch.txt", unpack=True, delimiter=",")
results = np.array(data)
sorted_results = results[:, results[2, :].argsort()]
apulse = sorted_results[4]
print(sorted_results[2])


def date_converter(dateinput):
    # October
    if dateinput < 191100:
        newdate = dateinput - 191022

    # November
    elif 191100 < dateinput < 191131:
        newdate = dateinput - 191091

    # December
    elif (dateinput > 191200) and (dateinput < 191232):
        newdate = dateinput - 191161


    # January
    elif (dateinput > 200100) and (dateinput < 200132):
        newdate = dateinput - 200030

    # February
    elif (dateinput > 200200) and (dateinput < 200230):
        newdate = dateinput - 200099

    #March
    elif (dateinput > 200300) and (dateinput < 200331):
        newdate = dateinput - 200170
    return newdate


Exposure = np.array([])

for item in sorted_results[2]:
    ndates = date_converter(item)
    Exposure = np.append(Exposure,ndates)

plt.errorbar(Exposure,apulse,marker='.',capsize=2, label="title", ls = 'none')
plt.xlabel('Exposure / days since 06/11/19')
plt.ylabel('Percentage of afterpulses')
##plt.ylim(0,1)
plt.title('Percentage of afterpulses vs Exposure (PMT Ch1 @ 1.4kV)')
plt.savefig('SummaryPlots/1400V/ApVsExp1_1400V.pdf')
plt.legend('')
plt.show()
