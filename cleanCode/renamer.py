import pandas as pd
import numpy as np

df = pd.read_csv('./csv_dateien/starcraftFinalcsvs/stackedRun.csv')

conditions = [
    (df['fraction'] == "P"),
    (df['fraction'] == "T"),
    (df['fraction'] == "Z"),
]

values = ["Protoss", "Terraner", "Zerg"]

df["fraction"] = np.select(conditions, values)

df.to_csv('./csv_dateien/starcraftFinalcsvs/stackedRun.csv')
