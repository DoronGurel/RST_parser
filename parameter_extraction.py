
import gensim
import numpy as np
import tree_builder, backprop
# dictFileName = '/Users/tal/Downloads/wiki-news-300d-1M.vec'
# embedding_dict = gensim.models.KeyedVectors.load_word2vec_format(dictFileName, binary=False)
# embedding_dict.save_word2vec_format(dictFileName+".bin", binary=True)

embedding_dict = gensim.models.KeyedVectors.load_word2vec_format('pretrained_word_vec/wiki-news-300d-1M.vec.bin', binary=True)


def get_is_leaf(node_1, node_2):
    ans = np.array([node_1.is_leaf(), node_2.is_leaf()], dtype=float)
    return ans


def get_nucliarity(node_1, node_2):
    ans = np.array([node_1.prop == 'Nucleus', node_2.prop == 'Nucleus'], dtype=float)
    return ans


def get_num_words(edu):
    return len(edu.split(' ')) -1

    # def get_first_word(edu):
    #     return edu[0]
    #

def get_mean_word_vec(edu):

    sum_embedding = np.zeros((1,300))
    for word in edu.split(' '):
        try:
            sum_embedding += np.array(embedding_dict[word])
        except:
            continue

    return sum_embedding.tolist()


def get_num_words(edu):
    return [len(edu.split(' ')) -1]


def get_dist_from_start_for_queue(edu,edu_list):
    return [edu_list.index(edu)]


def get_dist_from_start_for_stack(node):
    get_dist_from_start_for_stack
    return [node.eduspan[0]]


def get_dist_from_end_for_queue(edu,edu_list):
    return [len(edu_list) - edu_list.index(edu) -2]


def get_dist_from_end_for_stack(node,len_edu_list):
    return [len_edu_list - node.eduspan[1] - 1]


def get_dist_between_edus_for_stack(upper_node, lower_node):
    return [upper_node.eduspan[1] - lower_node.eduspan[1]]


def get_dist_between_edus_for_queue(edu, edu_list, node):
    return [node.eduspan[1] - edu_list.index(edu)+1]


def is_same_sentence_for_queue(edu, node,edu_list):
    for i in range(edu_list.index(edu),node.eduspan[0]-1):
        if (edu_list[i].endswith('.') or edu_list[i].endswith('."') or edu_list[i].endswith('. ')) \
                and (edu_list[i+1][0].isupper() or edu_list[i+1][1].isupper()):
            return [0]
    return [1]

def is_same_sentence_for_stack(node1, node2,edu_list):
    for i in range(node1.eduspan[0]-1,node2.eduspan[0]-1):
        print(edu_list[i])
        print(edu_list[i+1])
        print(edu_list[i].endswith('. '))
        if (edu_list[i].endswith('.') or edu_list[i].endswith('."') or edu_list[i].endswith('. ')) \
                and (edu_list[i + 1][0].isupper() or edu_list[i + 1][1].isupper()):
            return [0]
    return [1]

if __name__ == '__main__':
    # edu = 'cat dog worm'
    # vec = get_mean_word_vec(edu)
    # print(vec)
    filename = '0600.out.dis'
    edu_list = open('training_data/' + filename.split('.')[0]
                    + '.out.edus', 'r').read().replace('    ', '').split('\n')

    filename = 'training_data/0600.out.dis'
    T = tree_builder.buildtree_from_train(filename)
    # Binarize the RST tree
    T = tree_builder.binarizetree(T)
    # Back-propagating information from
    #   leaf node to root node
    T = backprop.backprop(T)
    list_of_nodes = backprop._BFTbin(T)

    # result = get_dist_from_start_for_queue(edu_list[1], edu_list)
    # print(result)
    # result = get_dist_from_start_for_stack(list_of_nodes[1])
    # print(list_of_nodes[1].eduspan)
    # print(result)
    # result = get_dist_from_end_for_stack(list_of_nodes[1], len(edu_list))
    # print(result)
    # result = get_dist_from_end_for_queue(edu_list[1], edu_list)
    # print(result)
    # print(list_of_nodes[1].eduspan)
    # print(list_of_nodes[3].eduspan)
    # result = get_dist_between_edus_for_stack(list_of_nodes[2], list_of_nodes[3])
    # print(result)
    # result = get_dist_between_edus_for_queue(edu_list[1], edu_list, list_of_nodes[1])
    # print(result)
    # result = is_same_sentence_for_stack(list_of_nodes[1], list_of_nodes[3], edu_list)
    # print(result)
    # result = is_same_sentence_for_queue(edu_list[0], list_of_nodes[3], edu_list)
    # print(result)