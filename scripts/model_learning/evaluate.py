import os
import sys
import pickle
import json
import pandas as pd
from sklearn.metrics import explained_variance_score

if len(sys.argv) != 3:
    sys.stderr.write("Arguments error. Usage:\n")
    sys.stderr.write("\tpython evaluate.py data-file model\n")
    sys.exit(1)

df = pd.read_csv(sys.argv[1])
X = df.drop(columns=["SalePrice"])  # Замените "SalePrice" на имя вашей целевой переменной
y = df["SalePrice"]  # Замените "SalePrice" на имя вашей целевой переменной

with open(sys.argv[2], "rb") as fd:
    clf = pickle.load(fd)

y_pred = clf.predict(X)
evs_score = explained_variance_score(y, y_pred)

prc_file = os.path.join("evaluate", "score.json")
os.makedirs(os.path.join("evaluate"), exist_ok=True)

with open(prc_file, "w") as fd:
    json.dump({"explained_variance_score": evs_score}, fd)