
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import dates as mdates
from scipy.optimize import curve_fit
import matplotlib.ticker as ticker
import datetime


dates = mdates.num2date(mdates.drange(datetime.datetime(2019, 10, 23),
                                      datetime.datetime(2020, 2, 23),
                                      datetime.timedelta(days=1)))




def linearfit(x,m,c):
    """
    :param x: data
    :param m: gradient const
    :param c: intercept
    """

    y = []
    for i in range(len(x)):
        y.append(m*x[i] + c)
    return y

def chi2(y_obs, y_err, y_exp, n_par):
    chi2 = 0
    ndof = len(y_obs) - n_par - 1
    for i in range(len(y_exp)):
        chi2 += ((y_exp[i] - y_obs[i])/y_err[i])**2
    chi2 = chi2/ndof
    return chi2

data = np.loadtxt("txtFiles/1000V/resolution_vs_date_Ch0_1kV.txt", unpack=True, delimiter=",")

results = np.array(data)
sorted_results = results[:, results[1, :].argsort()]

#VARIABLES
sigma = sorted_results[5]
sigma_err = sorted_results[6]
mu = sorted_results[3]
mu_err = sorted_results[4]
chisq = sorted_results[7]

#error_propogation
sigma_sq = ((sigma_err / sigma)**2)
mu_sq = ((mu_err / mu)**2)
sm_sq = np.sqrt((sigma_sq + mu_sq))

resolution = (sigma / mu) * 100
res_err = resolution * sm_sq

def date_plustwenty(dateinput):
    dateformat = dateinput + 20000000;
    return dateformat

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
    elif (dateinput > 200200) and (dateinput < 200229):
        newdate = dateinput - 200084
    return newdate


Exposure = np.array([])
formatted_dates = np.array([])

for item in sorted_results[1]:
    fdates = str(int(date_plustwenty(item)))
    datet = datetime.datetime.strptime(fdates, '%Y%m%d').strftime("%d/%m/%y")

    formatted_dates = np.append(formatted_dates,datet)

print(formatted_dates)

for item in sorted_results[1]:
    ndates = date_converter(item)
    Exposure = np.append(Exposure,ndates)


Exposure_l = Exposure[20:]
#Exposure_line = Exposure_l.reshape(-1,1)


resolution_line = resolution[20:]
res_err_line = res_err[20:]

p_guess = [0,3]
p_bounds = [[0,0],[10,10]]

popt, pcov = curve_fit(linearfit, Exposure_l, resolution_line, p0=p_guess, bounds=p_bounds)
print("The optimised fitted parameters are: ", popt)
print("The covariance matrix is: ", pcov)

for i in range(len(popt)):
    print("Error on parameter {}: {} is {}".format(i, popt[i], np.sqrt(pcov[i][i])))

chi2 = chi2(resolution_line, res_err_line, linearfit(resolution_line, *popt), 2)

print("The reduced chi2 is: ", chi2)

fig2, ax3 = plt.subplots()
color = 'tab:red'

ax3.set_xlabel("Exposure / days since 08/10/19")
ax3.set_ylabel("Resolution / %", color=color)
ax3.plot(Exposure_l, linearfit(Exposure_l,*popt), c='tab:blue')
ax3.errorbar(formatted_dates,resolution, yerr = res_err, marker = '.', color=color, capsize=2, label='title2', ls = 'none')
ax3.tick_params(axis='y', labelcolor=color)

ax4 = ax3.twinx()
color = 'tab:blue'
ax4.set_ylabel("Chi Squared Value", color=color)
ax4.errorbar(Exposure, chisq, marker='x', color=color, capsize=2, label = 'title', ls = 'none')
ax4.set_ylim(3,7)
ax4.tick_params(axis='y',labelcolor=color)

ax3.xaxis.set_major_locator(ticker.MaxNLocator(10))
ax3.xaxis.set_minor_locator(ticker.MaxNLocator(100))

fig2.autofmt_xdate()
plt.title('Resolution vs Exposure PMT Ch0')
plt.show()

######## Integer date plot ############
fig, ax1 = plt.subplots()
color = 'tab:red'


ax1.set_xlabel("Exposure / days since 23/10/19")
ax1.set_ylabel("Resolution / %", color=color)
ax1.plot(Exposure_l, linearfit(Exposure_l,*popt), c='tab:blue')
ax1.errorbar(Exposure,resolution, yerr = res_err, marker = '.', color=color, capsize=2, label = 'title', ls = 'none')
ax1.tick_params(axis='y', labelcolor=color)
ax2 = ax1.twinx()
color = 'tab:blue'
ax2.set_ylabel("Chi Squared Value", color=color)
ax2.errorbar(Exposure, chisq, marker='x', color=color, capsize=2, label = 'title', ls = 'none')
ax2.set_ylim(3,7)
ax2.tick_params(axis='y',labelcolor=color)

plt.text(100,4.5,"Chi sq: "+ str("%.2f"%chi2))

plt.title('Resolution vs Exposure PMT Ch0 @ 1kV')
plt.savefig('SummaryPlots/1000V/ResVsExp0_1kV.pdf')
plt.show()

fig3, ax5 = plt.subplots()
color = 'tab:blue'
ax5.set_ylabel("Mu value / pC")
ax5.errorbar(Exposure,mu, yerr = mu_err,marker=".", color=color, capsize=2, label ='title', ls = 'none')
plt.title('Mu vs Exposure PMT Ch0')
plt.savefig('SummaryPlots/1000V/MuVsExp0_1kV.pdf')
plt.show()

fig4, ax6 = plt.subplots()
color = 'tab:red'
ax6.set_ylabel("Sigma value")
ax6.errorbar(Exposure,sigma, yerr = sigma_err, marker=".",color=color, capsize=2, label = 'title',ls='none')
plt.title('Sigma vs Exposure PMT Ch0')
plt.savefig('SummaryPlots/1000V/SigmaVsExp0_1kV.pdf')
plt.show()