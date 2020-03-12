import numpy as np
from sklearn.linear_model import LinearRegression
import ResVsExp0

x = ResVsExp0.Exposure_line
y = ResVsExp0.resolution_line
y_err = ResVsExp0.res_err_line

WLS = LinearRegression()

print(WLS.fit(x,y,y_err))
c = WLS.intercept_
w = WLS.coef_[0]
ypred = w*x + c

ydiffsq = ((y-ypred)**2) / ypred

chisq = np.sum(ydiffsq)
print(chisq)


