import re

class Node(object):
    def __init__(self, role=None):
        self.text = None # Text of EDU, relevant if its a leaf node
        self.role = role # Nucleus or Satellite
        self.relation = None # relation of given span
        self.structure = None  # {Nucleus-Nucleus: NN, Nucleus-Satellite: NS, Satellite-Nucleus: SN}
        self.spanlimits = None # EDU span: [begin, end] index
            # for the binarization and tree-structure verification,
            # children are saved both as seperate attributes and as a list
        self.left = None # left child
        self.right = None # right child
        self.parent = None # parent node
        self.children = []

    def __repr__(self):
        return 'Node of Span: {}'.format(str(self.spanlimits))

    def extract_all_attributes(self):
        return self.role, self.text, self.relation, self.structure, self.spanlimits, self.left, self.right, self.parent, self.children

    def print_all_attributes(self):
        print(self.role, self.text, self.relation, self.structure, self.spanlimits, self.left, self.right, self.parent, self.children)

    def is_leaf(self):
        return self.spanlimits[0] == self.spanlimits[1]

def clean_and_tokenize_raw(text):

    # Receives all the text in a .dis file. Separates parentheses from other elements and turns the text into a list of tokens.
    # Then, the function changes textual parentheses into brackets to avoid interference with the tree_creator

    text = text.strip()
    text = text.replace('(', ' ( ')
    text = text.replace(')', ' ) ')
    text = text.replace('\n','')
    text = text.replace('//TT_ERR', '') # There are at least 2 files with this type of error
    tokens_list = text.split()
    tokens_copy = tokens_list[:]
    left_p, right_p, left_b, right_b ,rmarker = '(' , ')' , '[' , ']' , '\_!'
    marker_count = 0
    for i,t in enumerate(tokens_copy):
        marker_count += len(re.findall(rmarker, t))
        if marker_count % 2 == 1: # textual parentheses - not structural, therefore need to be changed to avoid interference with parser
            if left_p in t:
                t = t.replace(left_p,left_b)
            if right_p in t:
                t = t.replace(right_p,right_b)
            tokens_copy[i] = t
    # if tokens_copy==tokens_list:
    #     print 'tokens unchanged by cleaning'
    return tokens_copy

def tree_creator(text):  # input:

    # Receives the text from an entire .dis tree. as an input and transforms it into a list of tokens.
    # Tokens are added up into the tokens_list until a ')' (closing bracket) is hit.
    # Then, we go back until we hit a '(', inserting everything between them into a stack.
    # Upon going 'back', the last element we reach is the title, which tells us what info is held inside
    # the current set of tokens examined. For example, 'Root', 'span', 'Nucleus', etc.

    tokens_list = clean_and_tokenize_raw(text)
    stack = []
    while tokens_list:
        token = tokens_list.pop(0)  # handle current first token
        if token != ')':  # continue inserting elements from the tokens_list into the stack until a ')' is hit
            stack.append(token)
        elif token == ')':
            elements = []  # elements in the stack
            while stack:
                cur_element = stack.pop()  # pop last element
                elements.append(cur_element)
                if cur_element == '(':  # first bracket closer
                    break
            elements.reverse()  # Reverse to the original order, parse according to the first content word
            title = elements[1] # Defines the case we are handling
            elements = elements[2:]
            item = 0  # initiate an item that will be appended to the stack after parsing
            if title in ['Nucleus', 'Satellite', 'Root']:  # Node instance
                item = Node(role=title)  # 'declare' a Node instance
                for element in elements:  # update the node's attributes according to the elements
                    if isinstance(element, Node):
                        item.children.append(element)
                        element.parent = item
                    elif element[0] == 'relation':
                        item.relation = element[1]
                    elif element[0] == 'span':
                        item.spanlimits = [element[1], element[2]]
                    elif element[0] == 'leaf':
                        item.spanlimits = [element[1], element[1]]
                    elif element[0] == 'text':
                        item.text = element[1]

            elif title == 'text':  # unify all separated elements into one string
                unified_text = ''
                for word in elements:
                    word = word.replace("_!", "")
                    unified_text = unified_text + ' ' + word
                unified_text = unified_text[1:].lower()
                item = ('text', unified_text)

            elif title == 'rel2par':
                relation = elements[0]
                item = ('relation', relation)

            elif title == 'span':
                first = int(elements[0])
                last = int(elements[1])
                item = (title, first, last)

            elif title == 'leaf':
                ind = int(elements[0])
                item = (title, ind, ind)

            stack.append(item)
    return stack[-1]
