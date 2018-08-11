





def _BFTbin(tree):
    """ Breadth-first treavsal on binary RST tree
    :type tree: SpanNode instance
    :param tree: an binary RST tree
    """
    queue = [tree]
    bft_nodelist = []
    while queue:
        node = queue.pop(0)
        bft_nodelist.append(node)
        if node.lnode is not None:
            queue.append(node.lnode)
        if node.rnode is not None:
            queue.append(node.rnode)
    return bft_nodelist


def __getspaninfo(lnode, rnode):
    """ Get span size for parent node
    :type lnode,rnode: SpanNode instance
    :param lnode,rnode: Left/Right children nodes
    """
    try:
        eduspan = (lnode.eduspan[0], rnode.eduspan[1])
    except TypeError:
        print(lnode.prop, rnode.prop)
        print(lnode.nucspan, rnode.nucspan)
    return eduspan


def __getforminfo(lnode, rnode):
    """ Get Nucleus/Satellite form and Nucleus span
    :type lnode,rnode: SpanNode instance
    :param lnode,rnode: Left/Right children nodes
    """
    if (lnode.prop=='Nucleus') and (rnode.prop=='Satellite'):
        nucspan = lnode.eduspan
        form = 'NS'
    elif (lnode.prop=='Satellite') and (rnode.prop=='Nucleus'):
        nucspan = rnode.eduspan
        form = 'SN'
    elif (lnode.prop=='Nucleus') and (rnode.prop=='Nucleus'):
        nucspan = (lnode.eduspan[0], rnode.eduspan[1])
        form = 'NN'
    else:
        raise ValueError("")
    return (form, nucspan)


def __getrelationinfo(lnode, rnode):
    """ Get relation information
    :type lnode,rnode: SpanNode instance
    :param lnode,rnode: Left/Right children nodes
    """
    if (lnode.prop=='Nucleus') and (rnode.prop=='Nucleus'):
        relation = lnode.relation
    elif (lnode.prop=='Nucleus') and (rnode.prop=='Satellite'):
        relation = lnode.relation
    elif (lnode.prop=='Satellite') and (rnode.prop=='Nucleus'):
        relation = rnode.relation
    else:
        print('lnode.prop = {}, lnode.eduspan = {}'.format(lnode.prop, lnode.eduspan))
        print('rnode.prop = {}, lnode.eduspan = {}'.format(rnode.prop, rnode.eduspan))
        raise ValueError("Error when find relation for new node")
    return relation


def __gettextinfo(lnode, rnode):
    """ Get text span for parent node
    :type lnode,rnode: SpanNode instance
    :param lnode,rnode: Left/Right children nodes
    """
    text = lnode.text + " " + rnode.text
    return text




def backprop(tree):
    """ Starting from leaf node, propagating node
        information back to root node
    :type tree: SpanNode instance
    :param tree: an binary RST tree
    """
    treenodes = _BFTbin(tree)
    treenodes.reverse()
    for node in treenodes:
        if (node.lnode is not None) and (node.rnode is not None):
            # Non-leaf node
            node.eduspan = __getspaninfo(node.lnode, node.rnode)
            node.text = __gettextinfo(node.lnode, node.rnode)
            if node.relation is None:
                # If it is a new node
                if node.prop == 'Root':
                    pass
                else:
                    node.relation = __getrelationinfo(node.lnode, node.rnode)
            node.form, node.nucspan = __getforminfo(node.lnode, node.rnode)
        elif (node.lnode is None) and (node.rnode is not None):
            # Illegal node
            pass
        elif (node.lnode is not None) and (node.rnode is None):
            # Illegal node
            pass
        else:
            # Leaf node
            pass
    return treenodes[-1]


