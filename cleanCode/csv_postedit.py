import pandas as pd
import numpy as np

# die vier in csv_create entstandenen Datensätze werden zu einem gestacked

df1 = pd.read_csv('./csv_dateien/starcraftFinalcsvs/1stRun.csv')
df2 = pd.read_csv('./csv_dateien/starcraftFinalcsvs/2ndRun.csv')
df3 = pd.read_csv('./csv_dateien/starcraftFinalcsvs/3rdRun.csv')
df4 = pd.read_csv('./csv_dateien/starcraftFinalcsvs/4thRun.csv')

df = pd.concat([df1, df2, df3, df4])

# Fraktionskürzel durch echte Bezeichnung ersetzen
# Es hat sich als effizienter herausgestellt es im Nachhinein über pandas zu bearbeiten, als direkt während des csv create Prozesses

conditions = [
    (df['fraction'] == "P"),
    (df['fraction'] == "T"),
    (df['fraction'] == "Z"),
]

values = ["Protoss", "Terraner", "Zerg"]

df["fraction"] = np.select(conditions, values)

# Durch die Konkardination und die Umbenennungen sind ungewünschte Spalten entstanden
df = df.drop(columns=["Unnamed: 0", "Unnamed: 0.2", "Unnamed: 0.1"])

df.to_csv('./csv_dateien/starcraftFinalcsvs/stackedRun.csv')
