import sys
import os
import io
import pandas as pd

if len(sys.argv) != 2:
    sys.stderr.write("Arguments error. Usage:\n")
    sys.stderr.write("\tpython3 get_features.py data-file\n")
    sys.exit(1)

f_input = sys.argv[1]
f_output = os.path.join("datasets", "stage1", "train.csv")
os.makedirs(os.path.join("datasets", "stage1"), exist_ok=True)

def process_data(fd_in, fd_out):
    # Чтение данных из файла и удаление столбца 'Id'
    df = pd.read_csv(fd_in)
    df.drop(columns=['Id'], inplace=True)
    
    # Сохранение обработанных данных в новый файл
    df.to_csv(fd_out, index=False)

with io.open(f_input, encoding="utf8") as fd_in:
    with io.open(f_output, "w", encoding="utf8") as fd_out:
        process_data(fd_in, fd_out)