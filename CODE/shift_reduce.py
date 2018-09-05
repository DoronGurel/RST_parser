from CODE import dis_to_tree
from CODE import tree_to_dataset as ttd
import numpy as np


class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

    def peek(self):
        return self.items[len(self.items) - 1]


class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items) - 1]

    def peek2(self):
        return self.items[len(self.items) - 2]

    def size(self):
        return len(self.items)


def edus_parser(file_path):
    with open(file_path, "r") as f:
        nodes_lines = f.read().splitlines()
        edu_list = [i[1].strip() for i in enumerate(nodes_lines)]
        nodes_lines = [(i[0]+1, i[1].strip()) for i in enumerate(nodes_lines)]
        rst_queue = Queue()
        rst_stack = Stack()
        for edu in nodes_lines:
            rst_queue.enqueue(edu)
        return rst_queue, rst_stack, edu_list


def shift(queue,stack):
    edu = queue.dequeue()
    node = dis_to_tree.Node()
    node.spanlimits = [edu[0],edu[0]]
    node.text = edu[1]
    stack.push(node)


def reduce(queue, stack, nucliarity, relation_1, relation_2, relation_3):
    # todo: add parser type to input, so this function would be generic for any algorithm we use
    upper = stack.pop()
    lower = stack.pop()
    upper.role = nucliarity[0]
    lower.role = nucliarity[1]
    upper.relation = relation_2
    lower.relation = relation_3
    parent_node = dis_to_tree.Node()
    parent_node.left = lower
    parent_node.right = upper
    parent_node.children = [lower, upper]
    parent_node.spanlimits = [lower.spanlimits[0], upper.spanlimits[1]]
    parent_node.relation = relation_1
    lower.parent, upper.parent = parent_node, parent_node
    stack.push(parent_node)


def run_model(queue, stack, edu_list, model, inv_label_to_index, force_reduce, method):
    if force_reduce:
        queue_edu = []
    else:
        queue_edu = queue.peek()[1]

    params = ttd.edus_to_params(queue_edu, stack.peek(), stack.peek2(), edu_list, method)

    model_decision = model.predict_proba(np.array(params).reshape(1,-1))
    model_decision = np.argsort(model_decision, axis=1)[:, -2:]

    if inv_label_to_index[model_decision[0][0]].split('_')[0] == 'shift' and force_reduce:
        action = inv_label_to_index[model_decision[0][1]]
    else:
        action = inv_label_to_index[model_decision[0][0]]
        action.replace('-','_')

    if action.split('_')[0] == 'shift':
        shift(queue,stack)
    elif action.split('_')[0] == 'reduce':
        reduce(queue, stack, action.split('_')[1], action.split('_')[2], action.split('_')[3], action.split('_')[4])
    else:
        raise NameError('model has produced invalid action')

def shift_reduce_parser(queue, stack,edu_list , model, inv_label_to_index, method):
    # todo: add parser type to input, so this function would be generic for any algorithm we use
    if queue.size() == 0 and stack.size() == 0:
        return 'Invalid input'
    elif queue.size() == 0 and stack.size() == 1:
        return stack.peek()
    else:
        if stack.size() < 2:
            shift(queue, stack)
            return shift_reduce_parser(queue,stack, edu_list, model, inv_label_to_index, method)
        else:
            if queue.size() == 0:
                force_reduce = True
            else:
                force_reduce = False

            run_model(queue, stack, edu_list, model, inv_label_to_index, force_reduce, method)
            return shift_reduce_parser(queue, stack, edu_list, model, inv_label_to_index, method)

