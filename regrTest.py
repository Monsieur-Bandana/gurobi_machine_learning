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


x = historical_data["realSum"]
y = historical_data["guest_satisfaction_overall"]

print("executed")
plt.scatter(x, y)
