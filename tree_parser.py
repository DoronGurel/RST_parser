
from . import tree_builder, backprop

def _postorder_DFT(tree, nodelist):
    """ Post order traversal on binary RST tree
    :type tree: SpanNode instance
    :param tree: an binary RST tree
    :type nodelist: list
    :param nodelist: list of node in post order
    """
    if tree.lnode is not None:
        _postorder_DFT(tree.lnode, nodelist)
    if tree.rnode is not None:
        _postorder_DFT(tree.rnode, nodelist)
    nodelist.append(tree)
    return nodelist


def tree_to_dev(tree, dir, tree_num):
    post_nodelist = nnp.postorder_DFT(tree, [])
    txtfile = open('/Users/tal/Downloads/RST/rst_project/dataset/{}_pred/{}.txt'.format(dir, tree_num),'w+')
    for node in post_nodelist:
        if node.prop is None:
            continue
        if node.prop[0] != 'R':
            txtfile.write("{} {} {} {} \n".format(node.eduspan[0], node.eduspan[1], node.prop[0], node.relation.split('-')[0]))


def train_to_gold():
    for filename in os.listdir('../dataset/DEV'):
        if filename.endswith(".dis"):
            print(filename)
            text = open('../dataset/DEV/{}'.format(filename), 'r').read()
            # Build RST tree
            T = tree_builder.buildtree(text)
            # Binarize the RST tree
            T = tree_builder.binarizetree(T)
            # Back-propagating information from
            #   leaf node to root node
            T = backprop.backprop(T)
            file_prefix = filename.partition(".")[0]
            tree_to_dev(T, 'DEV3', file_prefix)



if __name__ == '__main__':
    train_to_gold()