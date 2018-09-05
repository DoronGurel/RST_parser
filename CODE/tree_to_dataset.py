import tree_parser, dis_to_tree, parameter_extraction
import numpy as np
import pandas as pd
import os

#constants
CONCATINATION = 'concat'
DIFFERENCE = 'diff'

def _flatten_list(alist):
    ans = []
    for item in alist:
        if isinstance(item, list):
            for subitem in item:
                ans.append(subitem)
        else:
            ans.append(item)

    return ans

def _get_nearest_left_node(node):
    stop = False
    ans = None
    while(node.parent is not None and not stop):
        if node.parent.right == node:
            stop =True
            ans = node.parent.left
        elif node.parent.left == node:
            node = node.parent
    return ans

def _get_two_nearest_left_nodes(node):
    counter = 0
    ans = []
    while(node.parent is not None and counter < 2):
        if node.parent.right == node:
            counter += 1
            ans.append(node.parent.left)
        node = node.parent
    ans += [None, None]
    return ans[0:2]

def tree_to_classification_decisions(tree, edu_list):
    list_of_nodes = tree_parser.reorder_nodes_for_gold(tree, children_list=[])
    list_of_decisions = []
    for node in list_of_nodes:
        if not node.is_leaf():
            list_of_decisions.append((edu_list[node.right.spanlimits[1]], node.left, node.right, 'reduce', node.left.role + node.right.role, str(node.relation) + '_' + str(node.left.relation) + '_' + str(node.right.relation)))
            if node.right.is_leaf():
                list_of_decisions.append((edu_list[node.right.spanlimits[1]-1], node.left, _get_nearest_left_node(node), 'shift', None, None))
            if node.left.is_leaf():
                stack_nodes = _get_two_nearest_left_nodes(node)
                list_of_decisions.append((edu_list[node.left.spanlimits[1]-1], stack_nodes[0], stack_nodes[1], 'shift', None, None))

    df_result = pd.DataFrame(list_of_decisions)
    df_result.columns = ['queue', 'stack_first', 'stack_second', 'decision', 'form', 'relation']
    return df_result

def edus_to_params(queue_edu, stack_first, stack_second, edu_list, method):
    # queue_params, stack_first_params, stack_second_params = [], [], []
    # get params for queue
    if len(queue_edu) > 1:
        queue_params = parameter_extraction.get_mean_word_vec(queue_edu)
        queue_params += parameter_extraction.get_num_words(queue_edu)
        queue_params += parameter_extraction.get_dist_from_start_for_queue(queue_edu, edu_list)
        queue_params += parameter_extraction.get_dist_from_end_for_queue(queue_edu, edu_list)

    else:
        queue_params = np.zeros([1,303]).tolist()

        # get params for stack first
    if stack_first is not None:
        if stack_first.text is not None:
            stack_first_params = parameter_extraction.get_mean_word_vec(stack_first.text)
            stack_first_params += parameter_extraction.get_num_words(stack_first.text)
            stack_first_params += parameter_extraction.get_dist_from_start_for_stack(stack_first)
            stack_first_params += parameter_extraction.get_dist_from_end_for_stack(stack_first, len(edu_list))
        else:
            stack_first_params = np.zeros([1,303]).tolist()
    else:
        stack_first_params = np.zeros([1,303]).tolist()

        # get params for stack second
    if stack_second is not None:
        if stack_second.text is not None:
            stack_second_params = parameter_extraction.get_mean_word_vec(stack_second.text)
            stack_second_params += parameter_extraction.get_num_words(stack_second.text)
            stack_second_params += parameter_extraction.get_dist_from_start_for_stack(stack_second)
            stack_second_params += parameter_extraction.get_dist_from_end_for_stack(stack_second, len(edu_list))
        else:
            stack_second_params = np.zeros([1,303]).tolist()
    else:
        stack_second_params = np.zeros([1,303]).tolist()

    queue_params = _flatten_list(queue_params)
    stack_first_params = _flatten_list(stack_first_params)
    stack_second_params = _flatten_list(stack_second_params)

    if method == CONCATINATION:
        final_params = np.concatenate([queue_params,stack_first_params,stack_second_params], axis=0).tolist()
    elif method == DIFFERENCE:
        first_diff = np.array(queue_params) - np.array(stack_first_params)
        second_diff = np.array(stack_first_params) - np.array(stack_second_params)

        final_params = np.concatenate([first_diff, second_diff], axis=0).tolist()
    else:
        raise Exception('unrecgnized method')

    return final_params

def class_decisions_to_dataset(df_decisions, edu_list, method):
    # todo: why do some nodes lack text?
    #
    final_dataset = []
    for index, row in df_decisions.iterrows():
        queue_edu = row['queue']
        stack_first = row['stack_first']
        stack_second = row['stack_second']

        final_params = edus_to_params(queue_edu, stack_first, stack_second, edu_list, method)
        final_params.append(row['decision'])
        final_params.append(row['form'])
        final_params.append(row['relation'])

        final_dataset.append(final_params)

    final_dataset = pd.DataFrame(final_dataset)

    return final_dataset

def train_to_dataset(method):
    tree_dataframes = []
    for filename in os.listdir('../dataset/TRAINING'):
        if filename.endswith(".dis"):
            print(filename)
            # Build RST tree
            text = open('../dataset/TRAINING/' + filename, 'r').read()
            T = dis_to_tree.tree_creator(text)
            # Binarize the RST tree
            tree_parser.right_binarization(T)
            tree_parser.verify_children_and_parenthood(T)

            if filename.split('.')[0] in ['file1', 'file2', 'file3', 'file4', 'file5']:
                edu_list = open('/Users/tal/Desktop/rst_parser_toolkit/dataset/TRAINING/' + filename.split('.')[0]
                                + '.edus', 'r').read().replace('    ', '').split('\n')
            else:
                edu_list = open('/Users/tal/Desktop/rst_parser_toolkit/dataset/TRAINING/' + filename.split('.')[0]
                                + '.out.edus', 'r').read().replace('    ', '').split('\n')

            decision_set = tree_to_classification_decisions(T, edu_list)
            tree_dataset = class_decisions_to_dataset(decision_set, edu_list, method)
            tree_dataframes.append(tree_dataset)

    total_dataset = pd.concat(tree_dataframes)
    total_dataset.to_csv('../dataset/shift_reduce_dataset_new_node.csv', index = False)

if __name__ == '__main__':

    tree_dataset = train_to_dataset(DIFFERENCE)
    # tree = tree_builder.buildtree_from_train('/Users/tal/Desktop/rst_parser_toolkit/TRAINING/1100.out.dis')
    # tree = tree_builder.binarizetree(tree)
    #
    # result = tree_to_classification_decisions(tree, edu_list)
    # result2 = class_decisions_to_dataset(result)
    # print(result2)
    # print(result['stack_first'][2].text)
    # print(result['stack_second'][2].text)
    # print(result['stack_second'][2].text + ' ' + result['stack_first'][2].text)

# for item in result:
    #     print(item)
        # vec1 = parameter_extraction.get_is_leaf(item[0], item[1])
        # vec2 = parameter_extraction.get_nucliarity(item[0], item[1])
        #
        # vec = np.concatenate((vec1,vec2))
        # print(vec)
        # # print(item[0].is_leaf(), item[1].is_leaf(), item[3])