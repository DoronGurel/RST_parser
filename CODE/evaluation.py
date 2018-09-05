import numpy as np
from os import listdir
from os.path import join

def load_tree(file_path):
    """
    :param file_path: path to file containing the serialized tree 
    :return: list of items that defines the full rehthorical structure of the tree
    """
    tree_strcture = []
    with open(file_path, "r") as f:
        nodes_lines = f.readlines()
    for line in nodes_lines:
        splited = line.rstrip().split(' ')
        ## Assert that the line format is valid
        assert len(splited) == 4, str.format("{} is in wrong format. Path: {}", line, file_path)
        assert splited[0].isdigit() and splited[1].isdigit() , str.format("{} contains node boundary which is not a number. Path: {}", line, file_path)
        from_idx = int(splited[0])
        to_idx = int(splited[1])
        nuc = splited[2]
        relation = splited[3]
        node  = ((from_idx, to_idx), nuc, relation)
        tree_strcture.append(node)

    return tree_strcture


def load_trees(folder_path):
    trees= {}
    files = listdir(folder_path)
    for file_name in files:
        full_path = join(folder_path, file_name)
        tree = load_tree(full_path)
        trees[file_name] = tree

    return trees





def eval_tree(gold_items, pred_items, idx):
    golds = [item[:idx] for item in gold_items]
    preds = [item[:idx] for item in pred_items]
    common = [item for item in golds if item in preds]

    return len(golds), len(preds), len(common)

def calc(num_gold, num_pred, num_common):
    p, r = 0, 0
    if num_pred == 0:
        p = 0
    else:
        p = float(num_common) / num_pred

    if num_gold == 0:
        r = 0
    else:
        r = float(num_common) / num_gold

    return p, r

def macro_f1(gold_trees, pred_trees):
    result = []
    for level in range(1, 4):
        prec = []
        recall = []
        for gold, pred in zip(gold_trees, pred_trees):
            num_gold, num_pred, num_common = eval_tree(gold, pred, level)
            p, r = calc(num_gold, num_pred, num_common)
            prec.append(p)
            recall.append(r)
        prec = np.array(prec).mean()
        recall = np.array(recall).mean()
        f1 = (2*prec*recall) / (prec+recall) if prec + recall > 0 else 0
        result.append(f1)
    return result

def eval(gold_trees_path, predicted_trees_path):
    """
    :param gold_trees_path: path to the folder containing to ground truth trees 
    :param predicted_trees_path: path to the folder containing the predicted trees
    """
    gold_trees = load_trees(gold_trees_path)
    predicted_trees = load_trees(predicted_trees_path)
    assert len(gold_trees) == len(predicted_trees), "Number of gold trees is not equal to number of predicted trees"
    ordered_gold_trees = []
    oredered_predicted_trees = []

    for g_name in gold_trees:
        assert g_name in predicted_trees, "Predicted trees are missing file: " + g_name
        gold_tree = gold_trees[g_name]
        predicted_tree = predicted_trees[g_name]
        assert len(gold_tree) == len(predicted_tree), "Size of predicted tree is not equal to size of gold tree for tree number: " + g_name
        ordered_gold_trees.append(gold_tree)
        oredered_predicted_trees.append(predicted_tree)
    macro_f1_result = macro_f1(ordered_gold_trees, oredered_predicted_trees)
    print (str.format("Span F1: {}", str(round(macro_f1_result[0] , 4))))
    print(str.format("Nuclearity F1: {}", str(round(macro_f1_result[1], 4))))
    print(str.format("Relation F1: {}", str(round(macro_f1_result[2], 4))))

def eval_inner(gold_trees_path, predicted_trees_path):
    """
    :param gold_trees_path: path to the folder containing to ground truth trees
    :param predicted_trees_path: path to the folder containing the predicted trees
    """
    gold_trees = load_trees(gold_trees_path)
    predicted_trees = load_trees(predicted_trees_path)
    assert len(gold_trees) == len(predicted_trees), "Number of gold trees is not equal to number of predicted trees"
    ordered_gold_trees = []
    oredered_predicted_trees = []

    for g_name in gold_trees:
        assert g_name in predicted_trees, "Predicted trees are missing file: " + g_name
        gold_tree = gold_trees[g_name]
        predicted_tree = predicted_trees[g_name]
        assert len(gold_tree) == len(predicted_tree), "Size of predicted tree is not equal to size of gold tree for tree number: " + g_name
        ordered_gold_trees.append(gold_tree)
        oredered_predicted_trees.append(predicted_tree)
    macro_f1_result = macro_f1(ordered_gold_trees, oredered_predicted_trees)
    return macro_f1_result

if __name__ == '__main__':
    import sys
    gold_trees_path = sys.argv[1]
    predicted_trees_path = sys.argv[2]
    eval(gold_trees_path, predicted_trees_path)
