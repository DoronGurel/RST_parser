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
from sklearn.metrics import f1_score
from sklearn.metrics import make_scorer
from sklearn.model_selection import GridSearchCV

f1_scorer = make_scorer(f1_score, average = 'weighted')

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

def logistic_regression_clf(dataset_file, model_file):
    df = concat_label("dataset/{}.csv".format(dataset_file))
    label_to_index = _label_to_index(df)
    df.iloc[:,-1] = df.iloc[:,-1].map(label_to_index).to_frame()

    lr_grid = {'C': [0.1,1], 'penalty' :['l2']}
    lr_clf = LogisticRegression(multi_class = 'multinomial', solver = 'lbfgs')
    lr_gs = GridSearchCV(lr_clf, lr_grid, scoring='f1_scorer', cv=4)
    lr_gs.fit(df.iloc[:,0:-1], df.iloc[:,-1])
    best_lr = lr_gs.best_estimator_
    results = lr_gs.cv_results_
    joblib.dump(best_lr, '{}.pkl'.format(model_file))
    np.save('label_to_index.npy', label_to_index)
    np.save('lr_results.npy', results)

def random_forest_clf(dataset_file, model_file):
    df = concat_label("dataset/{}.csv".format(dataset_file))
    label_to_index = _label_to_index(df)
    df.iloc[:,-1] = df.iloc[:,-1].map(label_to_index).to_frame()

    rf_grid = {'max_features': ['auto' ,0.1], 'n_estimators': [100]}
    rf_clf = RandomForestClassifier()
    rf_gs = GridSearchCV(rf_clf, rf_grid, scoring='f1_scorer', cv=4)
    rf_gs.fit(df.iloc[:,0:-1], df.iloc[:,-1])
    best_rf = rf_gs.best_estimator_
    results = rf_gs.cv_results_
    joblib.dump(best_rf, '{}.pkl'.format(model_file))
    np.save('rf_label_to_index.npy', label_to_index)
    np.save('rf_results.npy', results)

# def svm_clf():
#     df = concat_label("TRAINING/shift_reduce_dataset8.csv")
#     label_to_index = _label_to_index(df)
#     sv_clf = LinearSVC(multi_class= 'crammer_singer')
#     sv_clf.fit(df.iloc[:,0:-1], df.iloc[:,-1])
#     joblib.dump(rf_clf, 'svm.pkl')
#     np.save('svm_label_to_index.npy', label_to_index)

def neural_network_clf(df):
    nn_grid = {'activation ': ['tanh','relu']}
    nn_clf = MLPClassifier()
    nn_gs = GridSearchCV(nn_clf, nn_grid, scoring='f1_scorer', cv=4)
    nn_gs.fit(df.iloc[:,0:-1], df.iloc[:,-1])
    best_nn = nn_gs.best_estimator_
    results = nn_gs.cv_results_
    joblib.dump(best_nn, '{}.pkl'.format(model_file))
    np.save('nn_label_to_index.npy', label_to_index)
    np.save('nn_results.npy', results)
    return nn_clf

if __name__ == '__main__':
    svm_clf()





