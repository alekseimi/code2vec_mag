import pandas as pd
import numpy as np

df_vectors = pd.read_csv("apache_df.csv")
print(df_vectors)

df_data = pd.read_csv("E:\Šola\Code2VecJavaParser\csv_dump.csv")
print(df_data)

df_seq = [df_data, df_vectors]
df_combined = df_data.merge(df_vectors, left_index=True, right_index=True)
print(df_combined.head())

df_combined = df_combined.drop(['Unnamed: 0'], axis=1)
print(df_combined.head())
df_combined.to_csv("test_csv.csv")

df_new = pd.read_csv("test_csv.csv")
df_new.head()
