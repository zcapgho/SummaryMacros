import numpy as np
from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression
import pandas as pd
import statsmodels.api as sm
import seaborn as sns
from scipy.stats import chisquare
from scipy.optimize import curve_fit

data0 = np.loadtxt("txtFiles/1000V/resolution_vs_date_Ch0_Ratio.txt", unpack=True, delimiter=",")
data1 = np.loadtxt("txtFiles/1000V/resolution_vs_date_Ch1_Ratio.txt", unpack=True, delimiter=",")

results0 = np.array(data0)
results1 = np.array(data1)

sorted_results0 = results0[:, results0[1, :].argsort()]
sorted_results1 = results1[:, results1[1, :].argsort()]

#VARIABLES_0
sigma0 = sorted_results0[5]
sigma_err0 = sorted_results0[6]
mu0 = sorted_results0[3]
mu_err0 = sorted_results0[4]
chisq0 = sorted_results0[7]

#VARIABLES_1
sigma1 = sorted_results1[5]
sigma_err1 = sorted_results1[6]
mu1 = sorted_results1[3]
mu_err1 = sorted_results1[4]
chisq1 = sorted_results1[7]

#error_propogation_0
sigma_sq0 = ((sigma_err0 / sigma0)**2)
mu_sq0 = ((mu_err0 / mu0)**2)
sm_sq0 = np.sqrt((sigma_sq0 + mu_sq0))

resolution0 = (sigma0 / mu0) * 100
res_err0 = resolution0 * sm_sq0

#error_propogation_1
sigma_sq1 = ((sigma_err1 / sigma1)**2)
mu_sq1 = ((mu_err1 / mu1)**2)
sm_sq1 = np.sqrt((sigma_sq1 + mu_sq1))

resolution1 = (sigma1 / mu1) * 100
res_err1 = resolution1 * sm_sq1

#ratio res
resolution = resolution0 / resolution1
res0_sq = (res_err0/resolution0)**2
res1_sq = (res_err1/resolution1)**2

res_sq = np.sqrt(res0_sq + res1_sq)
res_err = resolution * res_sq


def date_converter(dateinput):
    # October
    if (dateinput < 191100):
       newdate = dateinput - 191022

    # November
    elif ((dateinput > 191100) and (dateinput < 191131)):
        newdate = dateinput - 191091

     # December
    elif ((dateinput > 191200) and (dateinput < 191232)):
        newdate = dateinput - 191161

    ##January
    elif ((dateinput > 200100) and (dateinput < 200132)):
        newdate = dateinput - 200030

        # February
    elif (dateinput > 200200) and (dateinput < 200230):
        newdate = dateinput - 200099

    return newdate

Exposure = np.array([])

for item in sorted_results0[1]:
    ndates = date_converter(item)
    Exposure = np.append(Exposure,ndates)

print(sorted_results0[1])

Exposure_l = Exposure[20:]
Exposure_line = Exposure_l.reshape(-1,1)

resolution_line = resolution[20:]
res_err_line = res_err[20:]

WLS = LinearRegression()
WLS.fit(Exposure_line,resolution_line,res_err_line)
w = WLS.coef_[0]
c = WLS.intercept_
r2 = WLS.score(Exposure_line,resolution_line)
print("The r^2 value is: ", r2)
print("The chi-square value is: ", chisquare(resolution_line))



plt.errorbar(Exposure,resolution, yerr = res_err, marker = '.', capsize=2, color='tab:red' ,label="title", ls = 'none')
plt.plot(Exposure_line, w*Exposure_line + c, c='tab:blue')
plt.xlabel('Exposure / days since 23/10/19')
plt.ylabel('Resolution Ratio')
##plt.ylim(0.5,1.1)
plt.title('Resolution Ratio of Channel 0 to Channel 1 vs Exposure')
plt.savefig('SummaryPlots/1000V/ResVsRatio.pdf')
plt.show()
