import pandas as pd
import numpy as np
import ast

table = pd.read_csv("training_data/shift_reduce_dataset3.csv")
number_of_features = len(ast.literal_eval(table['params'][0]))
features_df = pd.DataFrame(columns = [i for i in range(number_of_features)])
label_df = pd.DataFrame(columns = ['label'])

for i in range(len(table)):
    features = table.iloc[i]['params']
    label = table.iloc[i]['full_decision']
    row = ast.literal_eval(features)
    features_df.loc[i] = np.array(row)
    label_df.loc[i] = label

df = pd.concat([features_df,label_df], axis = 1)
df.to_csv("decisions_df.csv")
# print df