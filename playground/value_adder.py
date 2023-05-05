# in diesem File wird der Resourcenverbrauch errechnet und der csv Datei angefügt

import pandas as pd

df = pd.read_csv('./csv_dateien/starcraftFinalcsvs/stackedRun.csv')

df = df[df["total_army"] > 0]

# Durch die Konkardination ist eine ungewünschte Spalte entstanden
df = df.drop(columns=["Unnamed: 0"])

df["resource_mining"] = df["total_workers"]*0.4*df["time"]

print(df.head)

df.to_csv('./csv_dateien/starcraftFinalcsvs/stackedRun.csv')
