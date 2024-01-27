import pandas as pd

memory = pd.read_json("./model/memory/training.json")

memory.to_csv("./model/memory/training.csv", index=False)