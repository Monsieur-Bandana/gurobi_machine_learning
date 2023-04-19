import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor

import sys
import gurobipy as gp

from gurobi_ml import add_predictor_constr

import gurobipy_pandas as gppd

# Base URL for retrieving data
# TODO combine weekdays and weekends, add another column true false, if weekend
historical_data = pd.read_csv(
    "csv_dateien/amsterdam_weekends.csv", index_col=0
)


# classify our features between the ones that are fixed and the ones that will be
# part of the optimization problem


features = "dist"
target = "guest_satisfaction_overall"

dataSetOne = historical_data.iloc[:726, :]
dataSetTwo = historical_data.iloc[726:, :]
dataSetTwo = dataSetTwo[features]
dataSetTwo = dataSetTwo.drop(columns=['dist'])


# Run our regression
scaler = StandardScaler()
regression = LinearRegression()
pipe = make_pipeline(scaler, regression)
print("version 13 executed")
# print(dataSetOne.loc[:, features], dataSetOne.loc[:, target])
pipe.fit(X=np.array(dataSetOne[features]).reshape(-1, 1),
         y=np.array(dataSetOne[target]).reshape(-1, 1))

print("fetted model")
# Start with classical part of the model
m = gp.Model()
print("created model")
# The y variables are modeling the probability of enrollment of each student. They are indexed by students data
y = gppd.add_vars(m, dataSetTwo, name='satisfactory', lb=0.0, ub=100.0)
print("explained y")
# We add to studentsdata a column of variables to model the "merit" feature. Those variable are between 0 and 2.5.
# They are added directly to the data frame using the gppd extension.
dataSetTwo = dataSetTwo.gppd.add_vars(m, lb=100.0, name=features)
print("modeled price")
# We denote by x the (variable) "merit" feature
x = dataSetTwo[features]
print("created x")
# Make sure that studentsdata contains only the features column and in the right order
dataSetTwo = dataSetTwo.loc[:, features]

m.update()
print("updated model")
# Let's look at our features dataframe for the optimization
print(dataSetTwo[:10])
print("some stuff in 10")
m.setObjective(y.sum(), gp.GRB.MAXIMIZE)

m.update()
print("udated model")
pred_constr = add_predictor_constr(
    m, pipe, dataSetTwo, y
)
print("created predictor")
pred_constr.print_stats()

print("printed stats")
m.optimize()

print(
    "Maximum error in approximating the regression {:.6}".format(
        np.max(pred_constr.get_error())
    )
)

pred_constr.input_values

# plt.scatter(x, y)
