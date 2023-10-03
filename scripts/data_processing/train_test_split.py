import yaml
import sys
import os

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder

# Загрузите параметры разбивки из файла params.yaml
params = yaml.safe_load(open("params.yaml"))["split"]

if len(sys.argv) != 2:
    sys.stderr.write("Arguments error. Usage:\n")
    sys.stderr.write("\tpython3 train_test_split.py data-file\n")
    sys.exit(1)

f_input = sys.argv[1]
f_output_train = os.path.join("datasets", "stage3", "train.csv")
os.makedirs(os.path.join("datasets", "stage3"), exist_ok=True)
f_output_test = os.path.join("datasets", "stage3", "test.csv")
os.makedirs(os.path.join("datasets", "stage3"), exist_ok=True)

p_split_ratio = params["split_ratio"]  # Получите коэффициент разбивки из params.yaml

# Загрузите ваш датасет из f_input
df = pd.read_csv(f_input)

# Здесь необходимо определить, какие признаки являются X (факторами) и y (целевой переменной).
# Замените индексы и названия столбцов на ваши.
X = df.drop(columns=["SalePrice"])  # Замените "Target_Column_Name" на имя вашей целевой переменной
y = df["SalePrice"]  # Замените "Target_Column_Name" на имя вашей целевой переменной

# Разделяем числовые и категориальные признаки
categorical_columns = X.select_dtypes(include=['object']).columns
numeric_columns = X.select_dtypes(exclude=['object']).columns

# Нормализуем числовые признаки
scaler = StandardScaler()
X[numeric_columns] = scaler.fit_transform(X[numeric_columns])

# Кодируем категориальные признаки с помощью One-Hot Encoding
encoder = OneHotEncoder(drop='first', sparse_output=False)
encoded_categorical = encoder.fit_transform(X[categorical_columns])
encoded_categorical_df = pd.DataFrame(encoded_categorical, columns=encoder.get_feature_names_out(categorical_columns))

# Объединяем закодированные категориальные и нормализованные числовые признаки
X = pd.concat([encoded_categorical_df, X[numeric_columns]], axis=1)

# Разбиваем данные на тренировочную и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=p_split_ratio, stratify=None)

# Сохраняем тренировочные и тестовые выборки в отдельные файлы
train_data = pd.concat([y_train, X_train], axis=1)
test_data = pd.concat([y_test, X_test], axis=1)

train_data.to_csv(f_output_train, index=False)
test_data.to_csv(f_output_test, index=False)