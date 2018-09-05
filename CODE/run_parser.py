from CODE import shift_reduce, tree_parser, tree_to_dataset, modeling
import os
from sklearn.externals import joblib
import numpy as np


#constants
CONCATINATION = 'concat'
DIFFERENCE = 'diff'


## create training GOLD files
# tree_parser.parse_all_trees('TRAINING')

# create decision dataset
tree_to_dataset.train_to_dataset('first_last_pos',CONCATINATION)


#train selected model
# modeling.random_forest_clf('first_last_word','rf_first_last_word')

# # load trained model
# model =joblib.load('pretrained_models/random_forest.pkl')
# label_to_index = np.load('pretrained_models/rf_label_to_index.npy').item()
# inv_label_to_index = {v: k for k, v in label_to_index.items()}
#
# #run parser
# for filename in os.listdir('dataset/TRAINING'):
#     if filename.endswith(".edus"):
#         print(filename)
#         queue, stack, edu_list = shift_reduce.edus_parser('dataset/TRAINING/{}'.format(filename))
#         tree = shift_reduce.shift_reduce_parser(queue, stack, edu_list, model, inv_label_to_index, method='concat')
#         tree_parser.goldenize(tree, 'TRAINING', filename.split('.')[0], pred=True)