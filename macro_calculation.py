import pandas as pd
import numpy as np
from scipy import stats
import math
from sklearn import linear_model

#Importing default rate data
output = pd.read_excel("/home/bosko/Desktop/model-calculation/banks_europe.xlsx")

#Importing macroeconomic data
macro_data = pd.read_excel("/home/bosko/Desktop/model-calculation/macro_data.xlsx")

#Default rate transformation
output.rename(columns={'bad_rate': 'DR'}, inplace=True)
output.loc[output.DR == 0, 'DR'] = 0.00003
output['DR_TRANSFORMED'] = stats.norm.ppf(output.DR)
output['DR_mean'] = output.DR.mean()
output['DR_TRANSFORMED_m'] = output.DR_TRANSFORMED.mean()
output['DR_TRANSFORMED_v'] = np.var(output.DR_TRANSFORMED, ddof=1)
dr_trans_v = output.DR_TRANSFORMED_v
output['rho'] = dr_trans_v/(dr_trans_v+1)

#System risk factor calculation
dr_m_trans = stats.norm.ppf(output.DR_mean)
dr_trans = output.DR_TRANSFORMED
rho = output.rho
output['Z'] = (dr_m_trans-np.sqrt(1-rho)*dr_trans)/np.sqrt(rho)

#Transforming absolute macroeconomic variables: GDP and Property

GDP = macro_data.GDP
GDP_lag = macro_data.GDP.shift(1)
Property = macro_data.Property
Property_lag = macro_data.Property.shift(1)

macro_data['GDP_YoY'] = 100 * (GDP - GDP_lag)/GDP_lag
macro_data['Property_YoY'] = 100 * (Property - Property_lag)/Property_lag
macro_data.drop(columns=['GDP', 'Property'], inplace=True)
macro_data.rename(columns={'GDP_YoY': 'GDP', 'Property_YoY': 'Property'}, inplace=True)

#Creating lagged values of macroeconomic data
macro_data_lagged = pd.DataFrame()

for column in macro_data:
    if column != 'year':
            macro_data_lagged[column + str(1)] = macro_data[column].shift(1)
            macro_data_lagged[column + str(2)] = macro_data[column].shift(2)
            macro_data_lagged[column + str(3)] = macro_data[column].shift(3)
            macro_data_lagged[column + str(4)] = macro_data[column].shift(4)
            macro_data_lagged['year'] = macro_data['year']

output_for_regression = output.merge(macro_data_lagged, on='year')

print(output_for_regression)