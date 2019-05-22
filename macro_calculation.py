import pandas as pd
import numpy as np
from scipy import stats
import sklearn
import math

default_rate = pd.read_excel("/home/bosko/Desktop/macro/banks_europe.xlsx")
default_rate.rename(columns={'bad_rate': 'DR'}, inplace=True)
default_rate.loc[default_rate.DR == 0, 'DR'] = 0.00003
default_rate.loc[:, 'DR_TRANSFORMED'] = stats.norm.ppf(default_rate.DR)
default_rate.loc[:, 'DR_mean'] = default_rate.DR.mean()
default_rate.loc[:, 'DR_TRANSFORMED_mean'] = default_rate.DR_TRANSFORMED.mean()
default_rate.loc[:, 'DR_TRANSFORMED_var'] = np.var(default_rate.DR_TRANSFORMED, ddof=1)

dr_trans_v = default_rate.DR_TRANSFORMED_var
default_rate.loc[:, 'rho_derived'] = dr_trans_v/(dr_trans_v+1)

dr_m_qnorm = stats.norm.ppf(default_rate.DR_mean)
dr_qnorm = default_rate.DR_TRANSFORMED
rho = default_rate.rho_derived

default_rate.loc[:, 'z_5'] = (dr_m_qnorm-np.sqrt(1-rho)*dr_qnorm)/np.sqrt(rho)

print(default_rate)