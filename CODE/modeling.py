# import pandas as pd
# from sklearn.naive_bayes import BernoulliNB
#
# def naive_bayes_clf():
#     # Data Loading
#     df = pd.read_csv("TRAINING/shift_reduce_dataset8.csv")
#     print(df)
#     df.fillna(' ', inplace=True)
#     df['label'] = df.iloc[:,-3] + '_' + df.iloc[:,-2] + '_' + df.iloc[:,-1]
#     df.drop(df.columns[-4:-1], axis=1, inplace= True)
#
#     label_to_index = {}
#     for i, label in enumerate(df.iloc[:,909].unique()):
#         label_to_index[label] = i
#     df.iloc[:,-1] = df.iloc[:,-1].map(label_to_index).to_frame()
#     nb_clf = BernoulliNB()
#     nb_clf.fit(df.iloc[:,0:-1], df.iloc[:,-1])
#     return nb_clf, label_to_index


import pandas as pd
import numpy as np
from sklearn.naive_bayes import BernoulliNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.neural_network import MLPClassifier
from sklearn.externals import joblib

def concat_label(path):
    df = pd.read_csv(path)
    df.fillna(' ', inplace=True)
    df['label'] = df.iloc[:,-3] + '_' +df.iloc[:,-2] +'_' +df.iloc[:,-1]
    df.drop(df.columns[-4:-1], axis=1, inplace= True)
    return df

def _label_to_index(df):
    label_to_index = {}
    for i, label in enumerate(df['label'].unique()):
        label_to_index[label] = i
    return label_to_index

def naive_bayes_clf():
    df = concat_label("TRAINING/shift_reduce_dataset8.csv")
    label_to_index = _label_to_index(df)
    df.iloc[:,-1] = df.iloc[:,-1].map(label_to_index).to_frame()
    nb_clf = BernoulliNB()
    nb_clf.fit(df.iloc[:,0:-1], df.iloc[:,-1])
    return nb_clf

def logistic_regression_clf():
    df = concat_label("TRAINING/shift_reduce_dataset8.csv")
    label_to_index = _label_to_index(df)
    df.iloc[:,-1] = df.iloc[:,-1].map(label_to_index).to_frame()

    lr_clf = LogisticRegression(multi_class = 'multinomial', solver = 'lbfgs')
    lr_clf.fit(df.iloc[:,0:-1], df.iloc[:,-1])
    joblib.dump(lr_clf, 'log_reg.pkl')
    np.save('label_to_index.npy', label_to_index)
    # return lr_clf, label_to_index

def random_forest_clf():
    df = concat_label("TRAINING/shift_reduce_dataset8.csv")
    label_to_index = _label_to_index(df)
    df.iloc[:,-1] = df.iloc[:,-1].map(label_to_index).to_frame()
    rf_clf = RandomForestClassifier(n_estimators=10)
    rf_clf.fit(df.iloc[:,0:-1], df.iloc[:,-1])
    joblib.dump(rf_clf, 'random_forest.pkl')
    np.save('rf_label_to_index.npy', label_to_index)

def svm_clf():
    df = concat_label("TRAINING/shift_reduce_dataset8.csv")
    label_to_index = _label_to_index(df)
    sv_clf = LinearSVC(multi_class= 'crammer_singer')
    sv_clf.fit(df.iloc[:,0:-1], df.iloc[:,-1])
    joblib.dump(rf_clf, 'svm.pkl')
    np.save('svm_label_to_index.npy', label_to_index)

def neural_network_clf(df):
    nn_clf = MLPClassifier()
    nn_clf.fit(df.iloc[:,0:-1], df.iloc[:,-1])
    return nn_clf

if __name__ == '__main__':
    svm_clf()





