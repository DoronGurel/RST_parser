import shift_reduce, modeling, tree_parser
import os


#train selected model
model, label_to_index = modeling.naive_bayes_clf()

#run parser
for filename in os.listdir('training_data'):
    if filename.endswith(".edus"):
        print(filename)
        queue, stack, edu_list = shift_reduce.edus_parser('training_data/{}'.format(filename))
        inv_label_to_index = {v: k for k, v in label_to_index.items()}
        tree = shift_reduce.shift_reduce_parser(queue, stack, edu_list, model, inv_label_to_index)
        tree_parser.tree_to_dev(tree, 'test', filename.split('.')[0])