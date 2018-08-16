import tree_builder, backprop, parameter_extraction
import numpy as np
import pandas as pd
import os

def _get_nearest_left_node(node):
    stop = False
    ans = None
    while(node.pnode is not None and not stop):
        if node.pnode.rnode == node:
            stop =True
            ans = node.pnode.lnode
        elif node.pnode.lnode == node:
            node = node.pnode

    return ans

def _get_two_nearest_left_nodes(node):
    counter = 0
    ans = []
    while(node.pnode is not None and counter < 2):
        if node.pnode.rnode == node:
            counter += 1
            ans.append(node.pnode.lnode)
        node = node.pnode
    ans += [None, None]
    return ans[0:2]

def tree_to_classification_decisions(tree, edu_list):
    list_of_nodes = backprop._BFTbin(tree)
    list_of_decisions = []
    for node in list_of_nodes:
        if not node.is_leaf():
            list_of_decisions.append((edu_list[node.rnode.eduspan[1]], node.lnode, node.rnode, 'reduce', node.lnode.prop[0] + node.rnode.prop[0] , node.relation))
            if node.rnode.is_leaf():
                list_of_decisions.append((edu_list[node.rnode.eduspan[1]-1], node.lnode, _get_nearest_left_node(node), 'shift', None, None))
            if node.lnode.is_leaf():
                stack_nodes = _get_two_nearest_left_nodes(node)
                list_of_decisions.append((edu_list[node.lnode.eduspan[1]-1], stack_nodes[0], stack_nodes[1], 'shift', None, None))

    df_result = pd.DataFrame(list_of_decisions)
    df_result.columns = ['queue', 'stack_first', 'stack_second', 'decision', 'form', 'relation']
    return df_result


def class_decisions_to_dataset(df_decisions):
    # todo: why do some nodes lack text?
    #
    final_dataset = []

    for index, row in df_decisions.iterrows():
        queue_params, stack_first_params, stack_second_params = [], [], []

        # get params for queue
        queue_params.append(parameter_extraction.get_num_words(row['queue']))

        # get params for stack first
        if row['stack_first'] is not None:
            if row['stack_first'].text is not None:
                stack_first_params.append(parameter_extraction.get_num_words(row['stack_first'].text))
            else:
                stack_first_params.append(0)
        else:
            stack_first_params.append(0)

        # get params for stack second
        if row['stack_second'] is not None:
            if row['stack_second'].text is not None:
                stack_second_params.append(parameter_extraction.get_num_words(row['stack_second'].text))
            else:
                stack_second_params.append(0)
        else:
            stack_second_params.append(0)

        final_dataset.append((queue_params + stack_first_params + stack_second_params, row['decision'], row['form'], row['relation']))

    final_dataset = pd.DataFrame(final_dataset)
    final_dataset.columns = ['params', 'decision', 'form', 'relation']
    final_dataset = final_dataset.replace([None], [''], regex=True)
    final_dataset['full_decision'] = final_dataset['decision'] + '-' + final_dataset['form'] + '-' + final_dataset['relation']

    return final_dataset

def train_to_dataset():
    tree_dataframes = []
    for filename in os.listdir('../training_data'):
        if filename.endswith(".dis"):
            try:
                print(filename)
                # Build RST tree
                T = tree_builder.buildtree_from_train(filename)
                # Binarize the RST tree
                T = tree_builder.binarizetree(T)
                # Back-propagating information from
                #   leaf node to root node
                T = backprop.backprop(T)
                edu_list = open('../training_data/' + filename.split('.')[0]
                        + '.out.edus', 'r').read().replace('    ', '').split('\n')
                decision_set = tree_to_classification_decisions(T, edu_list)
                tree_dataset = class_decisions_to_dataset(decision_set)
                tree_dataframes.append(tree_dataset)
            except:
                continue

    total_dataset = pd.concat(tree_dataframes)
    total_dataset.to_csv('shift_reduce_dataset.csv')

if __name__ == '__main__':
    tree_dataset = train_to_dataset()
    # tree = tree_builder.buildtree_from_train('/Users/tal/Desktop/rst_parser_toolkit/training_data/1100.out.dis')
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