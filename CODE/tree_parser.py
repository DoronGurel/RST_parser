from dis_to_tree import *
import os
from utils import *

def print_all_children(node):
    print('working on node', node)
    children_list = node.children
    if children_list==[]:
        print('this is a leaf')
        return
    else:
        print(children_list)
        return print_all_children(children_list[0]),print_all_children(children_list[1])

def verify_children_and_parenthood(node):
    num_of_children = len(node.children)
    if num_of_children not in [0,2]:
        raise ValueError('tree not binarized')
    elif num_of_children==0:
        return
    elif num_of_children==2:
        # verify children
        node.left = node.children[0]
        node.right = node.children[1]
        # verify parenthood
        node.left.parent = node
        node.right.parent = node
        return verify_children_and_parenthood(node.left),verify_children_and_parenthood(node.right)


def synthesize_parent(L, R):
    '''
    a function used for the binarization process - creates a parent node for 
    2 nodes that were previously children of a node with more than 2 children'''
    p = Node(role=L.role)
    p.left = L
    p.right = R
    p.children = [L, R]
    p.spanlimits = [L.spanlimits[0], R.spanlimits[1]]

    if (L.role == 'Nucleus') and (R.role == 'Nucleus'):
        p.structure = 'NN'
        p.relation = L.relation
    elif (L.role == 'Nucleus') and (R.role == 'Satellite'):
        p.structure = 'NS'
        p.relation = L.relation
    elif (L.role == 'Satellite') and (R.role == 'Nucleus'):
        p.structure = 'SN'
        p.relation = R.relation

    return p

def right_binarization(node):
    '''
    There are three options for a given input node:
    opt (1): It has 0 children - it's a leaf, no binarization needed
    opt (2): It has 2 children - it's already binarized
    opt (3): It hs more than 2 children - in this case, we remove the 2 rightmost children,
    add a new node as their parent, and add this (now parent) node as the rightmost child of the input node.
    we do this iteratively until the input node is binary.

    After this, we send the right and left branches of the (possibly altered) input node
    into the same binarization process.
    '''

    num_of_children = len(node.children)
    # opt (1)
    if num_of_children==0:
        return
    # opt (2)
    elif num_of_children==2:
        left_branch = node.children[0] #node.left
        right_branch = node.children[1] #node.right
    # opt (3)
    elif num_of_children>2:
        children_list = [child for child in node.children]
        # Nullify current children of node
        node.children = []
        node.left = None
        node.right = None

        # as long as the input node still has more than 2 children, we need to keep binarizing
        while len(children_list)>2:
            # remove the 2 rightmost nodes
            first_from_right = children_list[-1]
            second_from_right = children_list[-2]
            children_list = children_list[:-2]
            new_parent = synthesize_parent(second_from_right,first_from_right)
            children_list.append(new_parent)
            first_from_right.parent = new_parent
            second_from_right.parent = new_parent
        # there are now only 2 nodes left, we can define them as the input node's new children
        right_branch = children_list[1]
        left_branch = children_list[0]
        node.children = children_list
        node.right = right_branch
        node.left = left_branch

    right_binarization(right_branch)
    right_binarization(left_branch)


def reorder_nodes_for_gold(node, children_list):
    children_list.append(node)
    if len(node.children)!=0:
        reorder_nodes_for_gold(node.children[0],children_list)
        reorder_nodes_for_gold(node.children[1], children_list)
    return children_list


def goldenize(tree, dir, tree_num):
    #turns an RST tree to a gold-structure file that can be evaluated via the evaluation code.
    ordered_for_gold = reorder_nodes_for_gold(tree, [])
    gold_file = open('../dataset/{}_GOLD/{}'.format(dir, tree_num),'w+')
    num=0 # test number of lines
    for node in ordered_for_gold:
        if node.role in ['Nucleus', 'Satellite']: # Node is not Root noe, which does not need to be printed
            num+=1
            span_left = node.spanlimits[0]
            span_right = node.spanlimits[1]
            role = node.role
            relation = map_to_cluster(node.relation)
            gold_file.write("{} {} {} {} \n".format(span_left, span_right, role, relation))
    # print 'num of rows is {}'.format(num)

def parse_all_trees(dir):
    # parses all the dis trees in a given directory, binarizes them and writes their gold-structure versions to seperate files.
    for file in os.listdir('../dataset/{}'.format(dir)):
        if file.endswith('.dis'):
            tree_num = file.partition(".")[0] # not all file names are numbers, some are 'file_{some_number}'.
            # print 'CURRENT TREE IS {}'.format(tree_num)
            if tree_num.startswith('file'):
                file_name = "../dataset/{}/{}.dis".format(dir, tree_num)
            else:
                file_name = "../dataset/{}/{}.out.dis".format(dir, tree_num)
            file_content = open(file_name, 'r').read()
            Tree = tree_creator(file_content)
            right_binarization(Tree)
            verify_children_and_parenthood(Tree)
            goldenize(Tree, dir, tree_num)
    print('Finished parsing and binarizing all {} trees'.format(dir))
# parse_all_trees('DEV')
parse_all_trees('TRAINING')

