import pandas as pd
import numpy as np

# die vier in csv_create entstandenen Datensätze werden zu einem gestacked

df = pd.read_csv('cleanCode/allRUnsButOnlyTerran.csv')


# Fraktionskürzel durch echte Bezeichnung ersetzen
# Es hat sich als effizienter herausgestellt es im Nachhinein über pandas zu bearbeiten, als direkt während des csv create Prozesses


conditions = [
    (df['fraction'] == "P"),
    (df['fraction'] == "T"),
    (df['fraction'] == "Z"),
]

values = ["Protoss", "Terraner", "Zerg"]

df["fraction"] = np.select(conditions, values)


# sc2reader zählt supply über das erlaubte limit hinaus
conditions2 = [
    (df['supply'] > 200.0),
]

values2 = [200.0]

df["supply"] = np.select(conditions2, values2)
# Durch die Konkardination und die Umbenennungen sind ungewünschte Spalten entstanden
df = df.drop(columns=["Unnamed: 0"])

df.to_csv('cleanCode/allRUnsButOnlyTerran.csv')
