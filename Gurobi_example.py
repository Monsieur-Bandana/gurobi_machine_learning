from sklearn.datasets import make_regression
from sklearn.metrics import mean_squared_error
from sklearn.neural_network import MLPRegressor
import numpy as np
import gurobipy as gp
from gurobi_ml import add_predictor_constr

X, y = make_regression(n_features=10, noise=1.0)

nn = MLPRegressor([20]*2, max_iter=10000, random_state=1)

nn.fit(X, y)

n = 2
index = np.random.choice(X.shape[0], n, replace=False)
X_examples = X[index, :]
y_examples = y[index]

m = gp.Model()

print(X_examples)

print(y_examples)

input_vars = m.addMVar(X_examples.shape, lb=X_examples-0.2, ub=X_examples+0.2)
output_vars = m.addMVar(y_examples.shape, lb=-gp.GRB.INFINITY)

pred_constr = add_predictor_constr(m, nn, input_vars, output_vars)

pred_constr.print_stats()

m.setObjective(output_vars@output_vars, gp.GRB.MINIMIZE)

m.optimize()

pred_constr.get_error()

output_vars.X

y_examples

pred_constr.remove()
