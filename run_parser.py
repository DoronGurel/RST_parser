import shift_reduce, tree_parser_old
import os
from sklearn.externals import joblib
import numpy as np

#train selected model
# model, label_to_index = modeling.logistic_regression_clf()
model =joblib.load('random_forest.pkl')
label_to_index = np.load('rf_label_to_index.npy').item()
inv_label_to_index = {v: k for k, v in label_to_index.items()}

#run parser
for filename in os.listdir('TRAINING'):
    if filename.endswith(".edus"):
        print(filename)
        queue, stack, edu_list = shift_reduce.edus_parser('TRAINING/{}'.format(filename))
        tree = shift_reduce.shift_reduce_parser(queue, stack, edu_list, model, inv_label_to_index)
        tree_parser_old.tree_to_dev(tree, 'test', filename.split('.')[0])