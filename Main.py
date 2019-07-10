# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals

from random import randrange

import io

from Util import Vertex

from WordnetParser import en_edges, de_edges

from WordnetParser import positive_words, negative_words

from DictParser import en_to_de, de_to_en


# parameters

max_steps = 20

num_walks = 100

required_ratio = 0.5

# output file: (had some silly unicode issues printing to standard out)

OUT_FILE_NAME = 'out.txt'



def walk_aggregate(word):
    """Given a word, run num_walks attempts
       of walking the network. Use the 
       averaged result of these attempts 
       to return a sentiment label for the word."""
    walk_results = []

    cur_node = word

    for attempt in range(num_walks):
        # check positive
        pos = walk_attempt(cur_node, positive_words)
        
        # check negative
        neg = walk_attempt(cur_node, negative_words)

        # store result of walk attempt
        walk_results.append((pos, neg))

    # compute averages from attempts
    pos_total, neg_total = 0, 0
    for pos_val, neg_val in walk_results: 
        pos_total += pos_val
        neg_total += neg_val

    pos_avg = pos_total / num_walks
    neg_avg = neg_total / num_walks


    # compare positive vs negative

    # label original word based on this
    if neg_avg < pos_avg:
        ratio = neg_avg / pos_avg
        if ratio < required_ratio:
            return "Negative"
    else:
        ratio = pos_avg / neg_avg
        if ratio < required_ratio:
            return "Positive"
    return "Neutral"



def walk_attempt(start_node, polarity_lexicon):
    """stochastic search through network until 
       a labeled node is encountered (only English nodes
       have labels) or until max_steps have been reached."""
    cur_node = start_node
    for step in range(max_steps):
        # figure out step options (available edges in-language and via translation)
        if cur_node.lang == "DE":
            options = de_edges[cur_node] + de_to_en[cur_node]
        elif cur_node.lang == "EN":
            options = en_edges[cur_node] + en_to_de[cur_node]
        else:
            assert False # only languages should be DE or EN
        assert options # if you can get there, you can get back
        cur_node = options[randrange(len(options))]
        if check_polarity(cur_node, polarity_lexicon):
            return step + 1  # (0th step is the start point)

    # expended all steps:
    return max_steps + 1


def check_polarity(vertex, lexicon):
    """takes a Vertex object and a lexicon and returns True if 
       the word from the vertex matches something in the lexicon.
       Returns False if no match is found or if the vertex is 
       for a non-english word"""
    if vertex.lang != "EN":
        return False
    return vertex.w in lexicon


if __name__ == "__main__":
    german_words = set()

    print "\nParameter Values:\nMax steps: {0}\nNum. walks: {1}\nRequired classification ratio: {2}" \
            .format(max_steps, num_walks, required_ratio)

    for key in de_edges:
        german_words.add(key)

    with io.open(OUT_FILE_NAME, 'w', encoding='utf-8') as f:
        for word in german_words:
            res = walk_aggregate(word)
            f.write("{0}\t{1}\t{2}\t{3}\n".format(word.w, word.pos, word.lang, res))
