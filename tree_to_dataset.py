import tree_builder, backprop, parameter_extraction
import numpy as np
import pandas as pd
import os

def _flat2gen(alist):
    for item in alist:
        if isinstance(item, list):
            for subitem in item: yield subitem
        else:
            yield item

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



def edus_to_params(queue_edu, stack_first, stack_second, edu_list):
    queue_params, stack_first_params, stack_second_params = [], [], []
    # get params for queue
    if len(queue_edu) > 1:
        queue_params.append(parameter_extraction.get_mean_word_vec(queue_edu))
        queue_params.append(parameter_extraction.get_num_words(queue_edu))
        queue_params.append(parameter_extraction.get_dist_from_start_for_queue(queue_edu, edu_list))
        queue_params.append(parameter_extraction.get_dist_from_end_for_queue(queue_edu, edu_list))

    else:
        queue_params += np.zeros([1,303]).tolist()

        # get params for stack first
    if stack_first is not None:
        if stack_first.text is not None:
            stack_first_params.append(parameter_extraction.get_mean_word_vec(stack_first.text))
            stack_first_params.append(parameter_extraction.get_num_words(stack_first.text))
            stack_first_params.append(parameter_extraction.get_dist_from_start_for_stack(stack_first))
            stack_first_params.append(parameter_extraction.get_dist_from_end_for_stack(stack_first, len(edu_list)))
        else:
            stack_first_params.append(np.zeros([1,303]).tolist())
    else:
        stack_first_params.append(np.zeros([1,303]).tolist())

        # get params for stack second
    if stack_second is not None:
        if stack_second.text is not None:
            stack_second_params.append(parameter_extraction.get_mean_word_vec(stack_second.text))
            stack_second_params.append(parameter_extraction.get_num_words(stack_second.text))
            stack_second_params.append(parameter_extraction.get_dist_from_start_for_stack(stack_second))
            stack_second_params.append(parameter_extraction.get_dist_from_end_for_stack(stack_second, len(edu_list)))
        else:
            stack_second_params.append(np.zeros([1,303]).tolist())
    else:
        stack_second_params.append(np.zeros([1,303]).tolist())

    queue_params = [y for x in queue_params for y in x]
    stack_first_params = [y for x in stack_first_params for y in x]
    stack_second_params = [y for x in stack_second_params for y in x]
    final_params = list(_flat2gen(queue_params + stack_first_params + stack_second_params))

    return final_params

def class_decisions_to_dataset(df_decisions, edu_list):
    # todo: why do some nodes lack text?
    #
    final_dataset = []
    for index, row in df_decisions.iterrows():
        queue_edu = row['queue']
        stack_first = row['stack_first']
        stack_second = row['stack_second']

        final_params = edus_to_params(queue_edu, stack_first, stack_second, edu_list)
        final_params.append(row['decision'])
        final_dataset.append(final_params)

    final_dataset = pd.DataFrame(final_dataset)
    # final_dataset.columns = ['params', 'decision', 'form', 'relation']
    # final_dataset = final_dataset.replace([None], [''], regex=True)
    # final_dataset['full_decision'] = final_dataset['decision'] + '-' + final_dataset['form'] + '-' + final_dataset['relation']

    return final_dataset

def train_to_dataset():
    tree_dataframes = []
    for filename in os.listdir('../training_data'):
        if filename.endswith(".dis"):
            # try:
            print(filename)
            # Build RST tree
            T = tree_builder.buildtree_from_train(filename)
            # Binarize the RST tree
            T = tree_builder.binarizetree(T)
            # Back-propagating information from
            #   leaf node to root node
            T = backprop.backprop(T)
            if filename.split('.')[0] in ['file1', 'file2', 'file3', 'file4', 'file5']:
                edu_list = open('/Users/tal/Desktop/rst_parser_toolkit/training_data/' + filename.split('.')[0]
                                + '.edus', 'r').read().replace('    ', '').split('\n')
            else:
                edu_list = open('/Users/tal/Desktop/rst_parser_toolkit/training_data/' + filename.split('.')[0]
                                + '.out.edus', 'r').read().replace('    ', '').split('\n')

            decision_set = tree_to_classification_decisions(T, edu_list)
            tree_dataset = class_decisions_to_dataset(decision_set, edu_list)
            tree_dataframes.append(tree_dataset)
            # except:
            #     continue

    total_dataset = pd.concat(tree_dataframes)
    total_dataset.to_csv('shift_reduce_dataset5.csv', index = False)

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