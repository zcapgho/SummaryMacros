import numpy as np
from matplotlib import pyplot as plt
from matplotlib import style
import math

data = np.loadtxt("txtFiles/1400V/apulseNUM_vs_date_Ch0_batch.txt", unpack=True, delimiter=",")
results = np.array(data)
sorted_results = results[:, results[2, :].argsort()]
apulse = sorted_results[4]
print(sorted_results[2])


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
        newdate = dateinput - 200084

    #march
    elif(dateinput > 200300) and (dateinput < 200331):
        newdate = dateinput - 200155

    return newdate

Exposure = np.array([])

for item in sorted_results[2]:
    ndates = date_converter(item)
    Exposure = np.append(Exposure,ndates)

print(Exposure)
print(apulse)


plt.errorbar(Exposure,apulse,marker='.',capsize=2, label="title", ls = 'none')
plt.xlabel('Exposure / days since 08/10/19')
plt.ylabel('Percentage of afterpulses')
#plt.ylim(0,1)
plt.title('Percentage of afterpulses vs Exposure (PMT Ch0 @ 1.4kV)')
plt.savefig('SummaryPlots/1400V/ApVsExp0_1400V.pdf')
plt.show()