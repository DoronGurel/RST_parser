import tree_builder, random_parser
import tree_to_dataset as ttd
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
    node = tree_builder.SpanNode()
    node.eduspan = (edu[0],edu[0])
    node.text = edu[1]
    stack.push(node)


def reduce(queue, stack):
    # todo: add parser type to input, so this function would be generic for any algorithm we use
    upper = stack.pop()
    lower = stack.pop()
    upper.prop,lower.prop = random_parser.random_nuclearity()
    upper.relation = random_parser.random_relation(upper.prop)
    lower.relation = random_parser.random_relation(lower.prop)
    parent_node = tree_builder.SpanNode()
    parent_node.lnode = lower
    parent_node.rnode = upper
    parent_node.eduspan = (lower.eduspan[0], upper.eduspan[1])
    lower.pnode, upper.pnode = parent_node, parent_node
    stack.push(parent_node)


def run_model(queue, stack, edu_list, model, inv_label_to_index):
    params = ttd.edus_to_params(queue.peek()[1], stack.peek(), stack.peek2(), edu_list)
    action = model.predict(np.array(params).reshape(1,-1))
    action = inv_label_to_index[action[0]]
    exec(action + '(queue, stack)')


def shift_reduce_parser(queue, stack,edu_list , model, inv_label_to_index):
    # todo: add parser type to input, so this function would be generic for any algorithm we use
    if queue.size() == 0 and stack.size() == 0:
        return 'Invalid input'
    elif queue.size() == 0 and stack.size() == 1:
        return stack.peek()
    else:
        if queue.size() == 0:
            reduce(queue, stack)
            return shift_reduce_parser(queue,stack, edu_list, model, inv_label_to_index)
        elif stack.size() < 2:
            shift(queue, stack)
            return shift_reduce_parser(queue,stack, edu_list, model, inv_label_to_index)
        else:
            run_model(queue, stack, edu_list, model, inv_label_to_index)
            return shift_reduce_parser(queue, stack, edu_list, model, inv_label_to_index)

