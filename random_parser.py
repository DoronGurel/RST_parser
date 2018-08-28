
import numpy as np
import os
from os import listdir
from os.path import join
import random
RELATION_LIST = ['ATTRIBUTION', 'BACKGROUND', 'CAUSE', 'COMPARISON', 'CONDITION', 'CONTRAST', 'ELABORATION', 'ENABLEMENT', 'TOPICCOMMENT', 'EVALUATION', 'EXPLANATION', 'JOINT', 'MANNERMEANS', 'SUMMARY', 'TEMPORAL', 'TOPICCHANGE', 'SPAN', 'SAME-UNIT', 'textualorganization']

def random_nuclearity():
    if np.random.rand() < 0.5:
        return 'N', 'S'
    else:
        return 'S', 'N'


def random_relation(nuclearity):
    if nuclearity == 'N':
        return 'span'
    else:
        return random.choice(RELATION_LIST).upper()


def random_shift_reduce():
    if np.random.rand() < 0.5:
        return 'shift'
    else:
        return 'reduce'





#
# for filename in os.listdir('../dataset/DEV'):
#     if filename.endswith(".edus"):
#         print('handeling file: {}'.format(filename))
#         # try:
#         file_prefix = filename.partition(".")[0]
#         queue, stack = edus_parser('../dataset/DEV/{}'.format(filename))
#         tree = shift_reduce_parser(queue, stack)
#         tree_to_dev2(tree, 'dev_random', file_prefix)
#         print("hi")
#         # except:
#         #     continue
# print('Finished!')