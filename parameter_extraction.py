
import gensim
import numpy as np
import tree_builder

# embedding_dict = gensim.models.KeyedVectors.load_word2vec_format('pretrained_word_vec/wiki-news-300d-1M.vec.bin', binary=True)


def get_is_leaf(node_1, node_2):
    ans = np.array([node_1.is_leaf(), node_2.is_leaf()], dtype=float)
    return ans

if __name__ == '__main__':
    # def get_num_words(edu):
    #     return len(edu)
    #
    # def get_first_word(edu):
    #     return edu[0]
    #
    # def get_mean_word_vec(edu):
    #  return false
    # dictFileName = '/Users/tal/Downloads/wiki-news-300d-1M.vec'
    # embedding_dict = gensim.models.KeyedVectors.load_word2vec_format(dictFileName, binary=False)
    # embedding_dict.save_word2vec_format(dictFileName+".bin", binary=True)
    # fname = "/Users/tal/Downloads/RST/rst_project/code/0600.out.edus"
    # text = open(fname, 'r').read()
    # tokens = text.strip().replace('    ','').split('\n')
    #
    # for token in tokens:
    #     new_token = token.replace('\n','').split(' ')
    #     new_token = [word for word in new_token if word != '']
    #
    #     mean_embedding = np.zeros((1,300))
    #     counter = 0
    #     for word in new_token:
    #         try:
    #             mean_embedding += np.array(embedding_dict[word])
    #             counter += 1
    #         except:
    #             continue
    #
    #     mean_embedding /= counter
    #     print(mean_embedding)