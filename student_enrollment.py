import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

import sys
import gurobipy as gp

from gurobi_ml import add_predictor_constr

import gurobipy_pandas as gppd

# Base URL for retrieving data
janos_data_url = "https://raw.githubusercontent.com/INFORMSJoC/2020.1023/master/data/"
historical_data = pd.read_csv(
    janos_data_url + "college_student_enroll-s1-1.csv", index_col=0
)

# classify our features between the ones that are fixed and the ones that will be
# part of the optimization problem
features = ["merit", "SAT", "GPA"]
target = "enroll"

# Run our regression
scaler = StandardScaler()
regression = LogisticRegression(random_state=1)
pipe = make_pipeline(scaler, regression)
pipe.fit(X=historical_data.loc[:, features], y=historical_data.loc[:, target])

# Retrieve new data used to build the optimization problem
studentsdata = pd.read_csv(
    janos_data_url + "college_applications6000.csv", index_col=0)

nstudents = 250

# Select randomly nstudents in the data
studentsdata = studentsdata.sample(nstudents)

# Start with classical part of the model
m = gp.Model()

# The y variables are modeling the probability of enrollment of each student. They are indexed by students data
y = gppd.add_vars(m, studentsdata, name='enroll_probability')

# We add to studentsdata a column of variables to model the "merit" feature. Those variable are between 0 and 2.5.
# They are added directly to the data frame using the gppd extension.
studentsdata = studentsdata.gppd.add_vars(m, lb=0.0, ub=2.5, name='merit')

# We denote by x the (variable) "merit" feature
x = studentsdata.loc[:, "merit"]

# Make sure that studentsdata contains only the features column and in the right order
studentsdata = studentsdata.loc[:, features]

m.update()

# Let's look at our features dataframe for the optimization
studentsdata[:10]

m.setObjective(y.sum(), gp.GRB.MAXIMIZE)

m.addConstr(x.sum() <= 0.2 * nstudents)
m.update()

pred_constr = add_predictor_constr(
    m, pipe, studentsdata, y, output_type="probability_1"
)

pred_constr.print_stats()

m.optimize()

print(
    "Maximum error in approximating the regression {:.6}".format(
        np.max(pred_constr.get_error())
    )
)

pred_constr.remove()

pwl_attributes = {
    "FuncPieces": -1,
    "FuncPieceLength": 0.01,
    "FuncPieceError": 1e-5,
    "FuncPieceRatio": -1.0,
}
pred_constr = add_predictor_constr(
    m, pipe, studentsdata, y, output_type="probability_1", pwl_attributes=pwl_attributes
)

m.optimize()

print(
    "Maximum error in approximating the regression {:.6}".format(
        np.max(pred_constr.get_error())
    )
)

pred_constr.input_values
