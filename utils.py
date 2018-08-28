import re


def map_to_cluster(relation):
    """
    :param relation: a string of original relation type from the RST-DT 
    :return: a string which is the clustered labl
    """
    lower_relation = relation.lower()
    if re.search(r'^attribution', lower_relation):
        cluster_relation = "ATTRIBUTION"

    elif re.search(r'^(background|circumstance)', lower_relation):
        cluster_relation = "BACKGROUND"

    elif re.search(r'^(cause|result|consequence)', lower_relation):
        cluster_relation = "CAUSE"

    elif re.search(r'^(comparison|preference|analogy|proportion)',
                   lower_relation):
        cluster_relation = "COMPARISON"

    elif re.search(r'^(condition|hypothetical|contingency|otherwise)',
                   lower_relation):
        cluster_relation = "CONDITION"

    elif re.search(r'^(contrast|concession|antithesis)', lower_relation):
        cluster_relation = "CONTRAST"

    elif re.search(r'^(elaboration.*|example|definition)', lower_relation):
        cluster_relation = "ELABORATION"

    elif re.search(r'^(purpose|enablement)', lower_relation):
        cluster_relation = "ENABLEMENT"

    elif re.search(
            r'^(problem\-solution|question\-answer|statement\-response|topic\-comment|comment\-topic|rhetorical\-question)',
            lower_relation):
        cluster_relation = "TOPICCOMMENT"

    elif re.search(r'^(evaluation|interpretation|conclusion|comment)',
                   lower_relation):
        cluster_relation = "EVALUATION"

    elif re.search(r'^(evidence|explanation.*|reason)', lower_relation):
        cluster_relation = "EXPLANATION"

    elif re.search(r'^(list|disjunction)', lower_relation):
        cluster_relation = "JOINT"

    elif re.search(r'^(manner|means)', lower_relation):
        cluster_relation = "MANNERMEANS"

    elif re.search(r'^(summary|restatement)', lower_relation):
        cluster_relation = "SUMMARY"

    elif re.search(r'^(temporal\-.*|sequence|inverted\-sequence)',
                   lower_relation):
        cluster_relation = "TEMPORAL"

    elif re.search(r'^(topic-.*)', lower_relation):
        cluster_relation = "TOPICCHANGE"

    elif re.search(r'^(span|same\-unit|textualorganization)$', lower_relation):
        cluster_relation = lower_relation.upper()

    else:
        raise ValueError(
                'unknown cluster_relation type in label: {}'.format(relation))

    return cluster_relation