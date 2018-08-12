import tree_builder, backprop, parameter_extraction
import numpy as np
import pandas as pd

def tree_to_classification_decisions(tree, edu_list):
    list_of_nodes = backprop._BFTbin(tree)
    list_of_decisions = []
    for node in list_of_nodes:
        if not node.is_leaf() and not node.is_root():
            list_of_decisions.append((edu_list[node.rnode.eduspan[1]],node.lnode, node.rnode, 'reduce', node.relation))

    df_result = pd.DataFrame(list_of_decisions)
    df_result.columns = ['queue', 'stack_top', 'stack_bottom', 'decision','sub_decision']
    return df_result


if __name__ == '__main__':
    tree = tree_builder.buildtree_from_train('/Users/tal/Desktop/rst_parser_toolkit/training_data/1101.out.dis')
    tree = tree_builder.binarizetree(tree)
    edu_list = open('/Users/tal/Desktop/rst_parser_toolkit/training_data/1101.out.edus', 'r').read().replace('    ', '').split('\n')
    result = tree_to_classification_decisions(tree, edu_list)


    print(result)
    # for item in result:
    #     print(item)
        # vec1 = parameter_extraction.get_is_leaf(item[0], item[1])
        # vec2 = parameter_extraction.get_nucliarity(item[0], item[1])
        #
        # vec = np.concatenate((vec1,vec2))
        # print(vec)
        # # print(item[0].is_leaf(), item[1].is_leaf(), item[3])