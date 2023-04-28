# optimizer with scaling and lin reg

import pandas as pd
import warnings
import gurobipy as gp
import matplotlib.pyplot as plt
from sklearn import tree
import seaborn as sns
import sklearn
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.metrics import r2_score
from sklearn.compose import make_column_transformer
import gurobipy_pandas as gppd
from gurobi_ml import add_predictor_constr

df = pd.read_csv('csv_dateien/starcraftFinalcsvs/stackedRun.csv')

df = df[:1350]

dfTerran = df[df["fraction"] == "T"]

X = dfTerran[["total_workers", "time"]]
y = dfTerran["resource_consumption"]

# Split the data for training and testing
X_train, X_test, y_train, y_test = train_test_split(
    X, y, train_size=0.8, random_state=1
)

feat_transform = make_column_transformer(
    (StandardScaler(), ["total_workers", "total_army"]),
)

scaler = StandardScaler()
lin_reg = make_pipeline(scaler, LinearRegression())
lin_reg.fit(X_train, y_train)

y_pred = lin_reg.predict(X_test)
print(f"The R^2 value in the test set is {r2_score(y_test, y_pred)}")

data = pd.read_csv('csv_dateien/starcraftFinalcsvs/3rdRun.csv')
dfTerranOpt = data[data["fraction"] == "T"]


# ,player,total_workers,total_army_value,total_army,fraction,winner,replay_filename
dfTerranOpt = dfTerranOpt.drop(columns=[
                               "total_workers", "player", "replay_filename", "winner", "fraction", "Unnamed: 0", "total_army"])

# create Model
m = gp.Model("Worker optimizer")

gppd.set_interactive()

# create variables
av = gppd.add_vars(m, lb=-gp.GRB.INFINITY,
                   pandas_obj=dfTerranOpt, name="total_army_value")
w = gppd.add_vars(m, pandas_obj=dfTerranOpt,
                  name="total_workers", vtype=gp.GRB.INTEGER)
r_ges = gppd.add_vars(m, pandas_obj=dfTerranOpt,
                      name="resource_consumption")
a = gppd.add_vars(m, pandas_obj=dfTerranOpt,
                  name="total_army", vtype=gp.GRB.INTEGER)
r_a = gppd.add_vars(m, pandas_obj=dfTerranOpt,
                    name="resource_per_unit")

m.update()
dfTerranOpt = dfTerranOpt.drop(columns=["resource_consumption"])

feats = dfTerranOpt
feats = pd.concat([w, feats], axis=1)
print(feats.head)
"""s#

m.setObjective((av/feats["time"]).sum(), gp.GRB.MAXIMIZE)
# m.setObjectiveN(w.sum(),1, gp.GRB.MINIMIZE)

gppd.add_constrs(m, w + feats["total_army"], gp.GRB.GREATER_EQUAL, 0)
gppd.add_constrs(m, w + feats["total_army"], gp.GRB.LESS_EQUAL, 200)

m.update()
feats = feats.drop(columns=["time"])
print(feats)
pred_constr = add_predictor_constr(m, lin_reg, feats, av)
# pred_constr = add_predictor_constr(m, lin_reg, feats, av)
pred_constr.print_stats()

# m.Params.NonConvex = 2

m.optimize()

print(w.gppd.X)

print(
    "Maximum error in approximating the regression {:.6}".format(
        np.max(pred_constr.get_error())
    )
)

outputs = pd.concat([pred_constr.input_values, av], axis=1)
print(outputs)






dfTerranOpt = dfTerranOpt.loc[:, features]

m.update()

dfTerranOpt[:10]





"""
