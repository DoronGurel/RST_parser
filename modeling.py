import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import BernoulliNB

def naive_bayes_clf():
    # Data Loading
    df = pd.read_csv("/Users/tal/Desktop/rst_parser_toolkit/training_data/shift_reduce_dataset4.csv")
    # print(df)
    # # Preprocessing
    # min_max_scaler = preprocessing.MinMaxScaler()
    # df.iloc[:,:-1] = min_max_scaler.fit_transform(df.iloc[:,:-1])
    # le = preprocessing.LabelEncoder()
    # le.fit(list(set(df.iloc[:,-1])))
    # df.iloc[:,-1] = le.transform(df.iloc[:,-1])
    #
    # # Train-Test split
    # X_train, X_test, y_train, y_test = train_test_split(df.iloc[:,:-1], df.iloc[:,-1], test_size=0.15, random_state=1)
    label_to_index = {}
    for i, label in enumerate(df.iloc[:,909].unique()):
        label_to_index[label] = i

    # df_extention = pd.DataFrame(label_to_index)
    # df.merge(df_extention, how = 'left', on = )
    print(label_to_index)

    df.iloc[:,-1] = df.iloc[:,-1].map(label_to_index).to_frame()
    # print(df['params'].tolist())
    # print(df)
    # train = []
    # label = []
    # for index, row in df.iterrows():
    #     # params = row['params'].replace('"','').replace('[','').replace(']','').split(',')
    #     train.append(np.array(row['params']))
    #     label.append(label_to_index[row['decision']])

    # label = df['decision'].map(label_to_index).to_frame()
    # train = df['params'].to_frame().as_matrix()
    # print(train)
    # Naive Bayes
    # print(df.drop(909,axis=1))
    nb_clf = BernoulliNB()
    nb_clf.fit(df.iloc[:,0:909], df.iloc[:,-1])

    return nb_clf, label_to_index

if __name__ == '__main__':
    naive_bayes_clf()
