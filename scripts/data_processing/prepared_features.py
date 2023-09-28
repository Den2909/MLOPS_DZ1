import sys
import os
import io
import pandas as pd

if len(sys.argv) != 2:
    sys.stderr.write("Arguments error. Usage:\n")
    sys.stderr.write("\tpython3 fill_na.py data-file\n")
    sys.exit(1)

f_input = sys.argv[1]
f_output = os.path.join("datasets", "stage2", "train.csv")
os.makedirs(os.path.join("datasets", "stage2"), exist_ok=True)

def process_data(fd_in, fd_out):
    # Чтение данных из файла
    df = pd.read_csv(fd_in)
    
    # Заполнение пропущенных значений в соответствии с вашими комментариями

    # Пропуски в признаке PoolQC
    df.loc[df['PoolArea'] == 0, 'PoolQC'] = 'No Pool'

    # Пропуски в признаке MiscFeature и MiscVal
    df.loc[(df["MiscVal"] == 0) & (df["MiscFeature"].isnull()), "MiscFeature"] = "No MiscFeature"

    # Пропуски в признаке Alley
    df['Alley'] = df['Alley'].fillna('No Alley')

    # Пропуски в признаке Fence
    df['Fence'] = df['Fence'].fillna('No Fence')

    # Пропуски в признаке FireplaceQu
    df.loc[df['Fireplaces'] == 0, 'FireplaceQu'] = 'No Fireplaces'

    # Заполнение пропусков в признаке LotFrontage
    df['LotFrontage'] = df.groupby('Neighborhood')['LotFrontage'].transform(lambda x: x.fillna(x.median()))

    # Пропуски в признаках GarageType, GarageFinish, GarageQual, GarageCond
    df.loc[df['GarageArea'] == 0, 'GarageYrBlt'] = 0
    cols_garag = ['GarageType', 'GarageFinish', 'GarageQual', 'GarageCond']
    for col in cols_garag:
        df.loc[(df['GarageArea'] == 0) & (df[col].isnull()), col] = 'No Garage'

    # Пропуски в признаках, связанных с подвалом
    df.loc[df['TotalBsmtSF'] == 0, 'BsmtFinSF1'] = 0
    cols_bsmt = ['BsmtCond', 'BsmtExposure', 'BsmtFinType1', 'BsmtQual']
    for col in cols_bsmt:
        df.loc[(df['TotalBsmtSF'] == 0) & (df[col].isnull()), col] = 'No Bsmt'

    # Пропуски в признаке BsmtFinType2
    df.loc[(df['BsmtFinSF2'] == 0) & (df['BsmtFinType2'].isnull()), 'BsmtFinType2'] = 'Unf'

    # Пропуски в признаках MasVnrArea и MasVnrType
    df['MasVnrArea'] = df['MasVnrArea'].fillna(0)
    df['MasVnrType'] = df['MasVnrType'].fillna('None')

    # Заполнение оставшихся единичных пропусков с использованием моды по районам
    columns_pass = ['BsmtExposure', 'BsmtFinType2', 'Electrical']

    def replacing_the_pass():
        mode = df.groupby('Neighborhood')[columns_na].agg(lambda x: x.value_counts().index[0])
        df[columns_na] = df[columns_na].fillna(df['Neighborhood'].map(mode))

    for columns_na in columns_pass:
        replacing_the_pass()
    
    
    df.drop(index=df[df['SalePrice'] > 500000].index, inplace=True)
    # Сохранение обработанных данных в новый файл
    df.to_csv(fd_out, index=False)

with io.open(f_input, encoding="utf8") as fd_in:
    with io.open(f_output, "w", encoding="utf8") as fd_out:
        process_data(fd_in, fd_out)