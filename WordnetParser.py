# -*- coding: utf-8 -*-
from __future__ import division

import io
from collections import defaultdict



from Util import german, english # constants
from Util import Vertex # data type representing node in graph

# script to initialize germanet, wordnet edges, as well as
# sets of english positive and negative words. 


DE_INPUT_FILE_NAME = "graphs/germanet.synonyms+hypernyms.wgraph13"

EN_INPUT_FILE_NAME = "eng_wordnet.txt"

POSITIVE_INPUT_FILE_NAME = "positive-words.txt"

NEGATIVE_INPUT_FILE_NAME = "negative-words.txt"
 
de_edges = defaultdict(list)

with io.open(DE_INPUT_FILE_NAME, 'r', encoding="utf-8") as f:
    for line in f:
        temp = line.split("\t")
        de_edges[Vertex(temp[1], temp[2], german)
                ].append(Vertex(temp[4], temp[5], german))
        de_edges[Vertex(temp[4], temp[5], german)
                ].append(Vertex(temp[1], temp[2], german))

        # make edges 2-way. Input file is not symmetric



en_edges = defaultdict(list)

with io.open(EN_INPUT_FILE_NAME, 'r', encoding="utf-8") as f:
    for line in f:
        temp = line.split("\t")
        en_edges[Vertex(temp[1], temp[2], english)
            ].append(Vertex(temp[4], temp[5], english)) 

        # input file is already symmetric



positive_words = set()

with io.open(POSITIVE_INPUT_FILE_NAME, 'r', encoding='utf-8') as f:
    lines = f.read().split("\n")
    positive_words = set(lines)


negative_words = set()
with io.open(NEGATIVE_INPUT_FILE_NAME, 'r', encoding='latin_1') as f:
    lines = f.read().split("\n")
    negative_words = set(lines)

