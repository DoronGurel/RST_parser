import os
## datastructure.py
## Author: Yangfeng Ji
## Date: 08-29-2013
## Time-stamp: <yangfeng 11/06/2014 14:40:27>

class SpanNode(object):
    """ RST tree node
    """
    def __init__(self, prop=None):
        """ Initialization of SpanNode
        :type prop: string
        :param prop: property of this span wrt its parent node.
                     Only two possible values: Nucleus or Satellite
        """
        # Text of this span / Discourse relation
        self.text, self.relation = None, None
        # EDU span / Nucleus span (begin, end) index
        self.eduspan, self.nucspan = None, None
        # Nucleus single EDU
        self.nucedu = None
        # Property: it is a Nucleus or Satellite
        self.prop = prop
        # Children node
        # Each of them is a node instance
        # N-S form (for binary RST tree only)
        self.lnode, self.rnode = None, None
        # Parent node
        self.pnode = None
        # Node list (for general RST tree only)
        self.nodelist = []
        # Relation form: NN, NS, SN
        self.form = None

    def is_leaf(self):
        return self.rnode is None and self.lnode is None and self.nodelist == []

    def is_root(self):
        return self.prop == 'Root'


def _createtext(lst):
    """ Create text from a list of tokens
    :type lst: list
    :param lst: list of tokens
    """
    newlst = []
    for item in lst:
        item = item.replace("_!","")
        newlst.append(item)
    text = ' '.join(newlst)
    # Lower-casing
    return text.lower()


def _processtext(tokens):
    """ Preprocessing token list for filtering '(' and ')' in text
    :type tokens: list
    :param tokens: list of tokens
    """
    identifier = '_!'
    within_text = False
    for (idx, tok) in enumerate(tokens):
        if identifier in tok:
            for _ in range(tok.count(identifier)):
                within_text = not within_text
        if ('(' in tok) and (within_text):
            tok = tok.replace('(','-LB-')
        if (')' in tok) and (within_text):
            tok = tok.replace(')','-RB-')
        tokens[idx] = tok
    return tokens


def _checkcontent(label, c):
    """ Check whether the content is legal
    :type label: string
    :param label: parsing label, such 'span', 'leaf'
    :type c: list
    :param c: list of tokens
    """
    if len(c) > 0:
        raise ValueError("{} with content={}".format(label, c))


def _createnode(node, content):
    """ Assign value to an SpanNode instance
    :type node: SpanNode instance
    :param node: A new node in an RST tree
    :type content: list
    :param content: content from stack
    """
    for c in content:
        # print 'type(c) = {}'.format(type(c))
        if isinstance(c, SpanNode):
            # Sub-node
            node.nodelist.append(c)
            c.pnode = node
        elif c[0] == 'span':
            node.eduspan = (c[1], c[2])
        elif c[0] == 'relation':
            node.relation = c[1]
        elif c[0] == 'leaf':
            node.eduspan = (c[1], c[1])
            node.nucspan = (c[1], c[1])
            node.nucedu = c[1]
        elif c[0] == 'text':
            node.text = c[1]
        else:
            raise ValueError("Unrecognized property: {}".format(c[0]))
    return node


def buildtree_from_train(dir):
    """ Build tree from *.dis file
    :type text: string
    :param text: RST tree read from a *.dis file
    """
    text = open(dir, 'r').read()
    tokens = text.strip().replace('//TT_ERR','').replace('\n','').replace('(', ' ( ').replace(')', ' ) ').split()
    # print 'tokens = {}'.format(tokens)
    queue = _processtext(tokens)
    # print 'queue = {}'.format(queue)
    stack = []
    while queue:
        token = queue.pop(0)
        if token == ')':
            # If ')', start processing
            content = [] # Content in the stack
            while stack:
                cont = stack.pop()
                if cont == '(':
                    break
                else:
                    content.append(cont)
            content.reverse() # Reverse to the original order
            # Parse according to the first content word
            if len(content) < 2:
                raise ValueError("content = {}".format(content))
            label = content.pop(0)
            if label == 'Root':
                node = SpanNode(prop=label)
                node = _createnode(node, content)
                stack.append(node)
            elif label == 'Nucleus':
                node = SpanNode(prop=label)
                node = _createnode(node, content)
                stack.append(node)
            elif label == 'Satellite':
                node = SpanNode(prop=label)
                node = _createnode(node, content)
                stack.append(node)
            elif label == 'span':
                # Merge
                beginindex = int(content.pop(0))
                endindex = int(content.pop(0))
                stack.append(('span', beginindex, endindex))
            elif label == 'leaf':
                # Merge
                eduindex = int(content.pop(0))
                _checkcontent(label, content)
                stack.append(('leaf', eduindex, eduindex))
            elif label == 'rel2par':
                # Merge
                relation = content.pop(0)
                _checkcontent(label, content)
                stack.append(('relation',relation))
            elif label == 'text':
                # Merge
                txt = _createtext(content)
                stack.append(('text', txt))
            else:
                raise ValueError("Unrecognized parsing label: {} \n\twith content = {}\n\tstack={}\n\tqueue={}".format(label, content, stack, queue))
        else:
            # else, keep push into the stack
            stack.append(token)
    # print 'stack = ', stack
    # print 'queue = ', queue
    # print 'stack[-1] = ', stack[-1].prop, stack[-1].eduspan
    # print 'stack[-2] = ', stack[-2].prop, stack[-2].eduspan
    return stack[-1]


def binarizetree(tree):
    """ Convert a general RST tree to a binary RST tree
    :type tree: instance of SpanNode
    :param tree: a general RST tree
    """
    queue = [tree]
    while queue:
        node = queue.pop(0)
        queue += node.nodelist
        # Construct binary tree
        if len(node.nodelist) == 2:
            node.lnode = node.nodelist[0]
            node.rnode = node.nodelist[1]
            # Parent node
            node.lnode.pnode = node
            node.rnode.pnode = node
        elif len(node.nodelist) > 2:
            # Remove one node from the nodelist
            node.lnode = node.nodelist.pop(0)
            newnode = SpanNode(node.nodelist[0].prop)
            newnode.nodelist += node.nodelist
            # Right-branching
            node.rnode = newnode
            # Parent node
            node.lnode.pnode = node
            node.rnode.pnode = node
            # Add to the head of the queue
            # So the code will keep branching
            # until the nodelist size is 2
            queue.insert(0, newnode)
        # Clear nodelist for the current node
        node.nodelist = []
    return tree




