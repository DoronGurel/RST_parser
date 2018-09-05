import numpy as np
import tree_builder, backprop
from CODE import parameter_extraction


def _dplp_param_extraction(queue, stack, edu_list):
    queue_edu = queue.peek()
    stack_first = stack.peek()
    stack_second = stack.peek2()

    queue_params, stack_first_params, stack_second_params = [], [], []
    queue_params.append(parameter_extraction.get_mean_word_vec(queue_edu))
    queue_params.append(parameter_extraction.get_num_words(queue_edu))
    queue_params.append(parameter_extraction.get_dist_from_start_for_queue(queue_edu, edu_list))
    queue_params.append(parameter_extraction.get_dist_from_end_for_queue(queue_edu, edu_list))

    # get params for stack first
    if stack_first.text is not None:
        stack_first_params.append(parameter_extraction.get_mean_word_vec(stack_first.text))
        stack_first_params.append(parameter_extraction.get_num_words(stack_first.text))
        stack_first_params.append(parameter_extraction.get_dist_from_start_for_stack(stack_first.text, edu_list))
        stack_first_params.append(parameter_extraction.get_dist_from_start_for_stack(stack_first.text, edu_list))
    else:
        stack_first_params += np.zeros([1,303]).tolist()


    # get params for stack second
    if stack_second.text is not None:
        stack_second_params.append(parameter_extraction.get_mean_word_vec(stack_second.text))
        stack_second_params.append(parameter_extraction.get_num_words(stack_second.text))
        stack_second_params.append(parameter_extraction.get_dist_from_start_for_stack(stack_second.text, edu_list))
        stack_second_params.append(parameter_extraction.get_dist_from_start_for_stack(stack_second.text, edu_list))
    else:
        stack_second_params += np.zeros([1,303]).tolist()

    return queue_params + stack_first_params + stack_second_params


def dplp_shift_reduce(queue, stack, edu_list):
    params = _dplp_param_extraction(queue,stack,edu_list)
    action = model_query(params)

    return action


if __name__ == '__main__':

    for filename in os.listdir('../TRAINING'):
        if filename.endswith(".dis"):
            try:
                print(filename)
                # Build RST tree
                T = tree_builder.buildtree_from_train(filename)
                # Binarize the RST tree
                T = tree_builder.binarizetree(T)
                # Back-propagating information from
                #   leaf node to root node
                T = backprop.backprop(T)
                edu_list = open('/Users/tal/Desktop/rst_parser_toolkit/TRAINING/' + filename.split('.')[0]
                                + '.out.edus', 'r').read().replace('    ', '').split('\n')
                decision_set = tree_to_classification_decisions(T, edu_list)
                tree_dataset = class_decisions_to_dataset(decision_set, edu_list)

_dplp_param_extraction()