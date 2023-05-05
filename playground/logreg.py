# Ermitteln welche Fraktion die stärkste Korrelation hat

import pandas as pd

import numpy as np
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
from sklearn.linear_model import LogisticRegression

df = pd.read_csv('csv_dateien/starcraftFinalcsvs/stackedRun.csv')

findoutx = "worker_army_ratio"
findouty = "army_in_time"

df = df[df["time"] > 0]

df["army_in_time"] = df["total_army_value"]/df["time"]
df["worker_army_ratio"] = df["total_army"]/df["total_workers"]

conditions = [
    (df['time'] <= 660),
    (df['time'] > 660),
]

values = [1, 0]

df["phase"] = np.select(conditions, values)


dfTerran = df[df["fraction"] == "T"]

X = dfTerran[["total_workers", "total_army"]]
y = dfTerran["total_army_value"]

# Split the data for training and testing
X_train, X_test, y_train, y_test = train_test_split(
    X, y, train_size=0.8, random_state=1
)

feat_transform = make_column_transformer(
    (StandardScaler(), ["total_workers", "total_army"]),
)

scaler = StandardScaler()
lin_reg = make_pipeline(scaler, LogisticRegression(random_state=1))
lin_reg.fit(X_train, y_train)

y_pred = lin_reg.predict(X_test)
print(f"The R^2 value in the test set is {r2_score(y_test, y_pred)}")

data = pd.read_csv('csv_dateien/starcraftFinalcsvs/3rdRun.csv')
dfTerranOpt = data[data["fraction"] == "T"]


# ,player,total_workers,total_army_value,total_army,fraction,winner,replay_filename
dfTerranOpt = dfTerranOpt.drop(columns=[
                               "total_workers", "player", "replay_filename", "winner", "fraction", "Unnamed: 0"])

# create Model
m = gp.Model("Worker optimizer")

gppd.set_interactive()

# create variables
av = gppd.add_vars(m, lb=-gp.GRB.INFINITY,
                   pandas_obj=dfTerranOpt, name="total_army_value")
w = gppd.add_vars(m, pandas_obj=dfTerranOpt,
                  name="total_workers", vtype=gp.GRB.INTEGER)

m.update()


dfTerranOpt = dfTerranOpt.drop(columns=["total_army_value"])
feats = dfTerranOpt
feats = pd.concat([w, feats], axis=1)
print(feats.head)

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
