from __future__ import division, unicode_literals

import io
from itertools import combinations

from nltk import wordnet as wn 

FILENAME = "eng_wordnet.txt"


FMT_STRING = "1\t{0}\t{1}\tEN\t{2}\t{3}\tEN\n"     # similar format as other files
             #   w1  pos       w2    pos

# interface with wordnet, compile in-synset, hypernym, and similar_to relations
# to output file. These will be symmetric (even though that isn't really necessary)

if __name__ == "__main__":
    with io.open(FILENAME, "w", encoding="utf-8") as f:

        edges = set()
        for synset in wn.wordnet.all_synsets():
            pos1 = synset.pos()
            lemma_combs = combinations(synset.lemma_names(), 2)
            for w1, w2 in lemma_combs:
                if w1 != w2:
                    edges.add((w1, pos1, w2, pos1))
                    edges.add((w2, pos1, w1, pos1)) # make everything symmetric
            # write all of these permutations + pos 
            for hyp in synset.hypernyms():
                pos2 = hyp.pos()
                hyp_combs = combinations(synset.lemma_names() + hyp.lemma_names() , 2)
                # write these
                for w1, w2 in hyp_combs:
                    if w1 != w2 or pos1 != pos2:
                        edges.add((w1, pos1, w2, pos2))
                        edges.add((w2, pos2, w1, pos1))

            for sim_to in synset.similar_tos():
                pos2 = sim_to.pos()
                sim_combs = combinations(synset.lemma_names() + sim_to.lemma_names(), 2)
                # write them
                for w1, w2 in sim_combs:
                    if w1 != w2 or pos1 != pos2:
                        edges.add((w1, pos1, w2, pos2))
                        edges.add((w2, pos2, w1, pos1))
                        
        for edge in edges:
            f.write(FMT_STRING.format(edge[0], edge[1], edge[2], edge[3]))



