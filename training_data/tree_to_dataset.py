import tree_builder, backprop, parameter_extraction

def tree_to_classification_decisions(tree):
    list_of_nodes = backprop._BFTbin(tree)
    list_of_decisions = []
    for node in list_of_nodes:
        if not node.is_leaf() and not node.is_root():
            list_of_decisions.append((node.lnode, node.rnode, 'reduce', node.relation))
    return list_of_decisions


if __name__ == '__main__':
    tree = tree_builder.buildtree_from_train('/Users/tal/Desktop/rst_parser_toolkit/training_data/1106.out.dis')
    tree = tree_builder.binarizetree(tree)
    result = tree_to_classification_decisions(tree)
    for item in result:
        print(item)
        print(parameter_extraction.get_is_leaf(item[0], item[1]))

        # print(item[0].is_leaf(), item[1].is_leaf(), item[3])