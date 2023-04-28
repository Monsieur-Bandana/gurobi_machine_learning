# Dieses File ist zum zusammenfügen der vier enstandenen Datnsätz zuständig

import pandas as pd

df1 = pd.read_csv('./csv_dateien/starcraftFinalcsvs/1stRun.csv')
df2 = pd.read_csv('./csv_dateien/starcraftFinalcsvs/2ndRun.csv')
df3 = pd.read_csv('./csv_dateien/starcraftFinalcsvs/3rdRun.csv')
df4 = pd.read_csv('./csv_dateien/starcraftFinalcsvs/4thRun.csv')

df = pd.concat([df1, df2, df3, df4])

# Durch die Konkardination ist eine ungewünschte Spalte entstanden
df = df.drop(columns=["Unnamed: 0"])

df.to_csv('./csv_dateien/starcraftFinalcsvs/stackedRun.csv')
