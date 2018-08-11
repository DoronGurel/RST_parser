
def decodeSRaction(tree):
    """ Decoding Shift-reduce actions from an binary RST tree
    :type tree: SpanNode instance
    :param tree: an binary RST tree
    """
    # Start decoding
    post_nodelist = postorder_DFT(tree, [])
    # print len(post_nodelist)
    actionlist = []
    for node in post_nodelist:
        if (node.lnode is None) and (node.rnode is None):
            actionlist.append(('Shift', None, None))
        elif (node.lnode is not None) and (node.rnode is not None):
            form = node.form
            if (form == 'NN') or (form == 'NS'):
                relation = extractrelation(node.rnode.relation)
            else:
                relation = extractrelation(node.lnode.relation)
            actionlist.append(('Reduce', form, relation))
        else:
            raise ValueError("Can not decode Shift-Reduce action")
    return actionlist


def getedunode(tree):
    """ Get all left nodes. It can be used for generating training
        examples from gold RST tree
    :type tree: SpanNode instance
    :param tree: an binary RST tree
    """
    # Post-order depth-first traversal
    post_nodelist = postorder_DFT(tree, [])
    # EDU list
    edulist = []
    for node in post_nodelist:
        if (node.lnode is None) and (node.rnode is None):
            edulist.append(node)
    return edulist







class ParseError(Exception):
    """ Exception for parsing
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class ActionError(Exception):
    """ Exception for illegal parsing action
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def extractrelation(s, level=0):
    """ Extract discourse relation on different level
    """
    return s.lower().split('-')[0]


def BFT(tree):
    """ Breadth-first treavsal on general RST tree
    :type tree: SpanNode instance
    :param tree: an general RST tree
    """
    queue = [tree]
    bft_nodelist = []
    while queue:
        node = queue.pop(0)
        bft_nodelist.append(node)
        queue += node.nodelist
    return bft_nodelist
