#!/usr/bin/python3

import gdown
import os
import pandas as pd

# URL для файла train.csv
url_train = 'https://drive.google.com/file/d/1VEiM8KPoqr2bF500a6XxsLssWJcoYHAy/view?usp=sharing'
file_id_train = url_train.split('/')[-2]
train = 'https://drive.google.com/uc?id=' + file_id_train

# URL для файла test.csv
url_test = 'https://drive.google.com/file/d/1yD1sTtI0S-Y-jaxOVCQjuEVjv7NDh5ZA/view?usp=sharing'
file_id_test = url_test.split('/')[-2]
test = 'https://drive.google.com/uc?id=' + file_id_test


datasets_dir = os.path.expanduser('~/Projects/MLOPS_DZ1/datasets')

if not os.path.exists(datasets_dir):
    os.makedirs(datasets_dir)

train_csv_path = os.path.join(datasets_dir, 'train.csv')
test_csv_path = os.path.join(datasets_dir, 'test.csv')

gdown.download(train, train_csv_path, quiet=False)
gdown.download(test, test_csv_path, quiet=False)

print("Файлы успешно скачаны и сохранены в папке datasets:", datasets_dir)
