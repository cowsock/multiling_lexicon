# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals

import io
from collections import defaultdict

INPUT_FILE_NAME = "ende-dict-cc.wgraph13"

from Util import Vertex, english, german

# load translation dictionary
# multiple translation targets are possible (hence mapping str -> list)


en_to_de = defaultdict(list)

de_to_en = defaultdict(list)

with io.open(INPUT_FILE_NAME, encoding='utf-8') as f:
    prev_line = ""
    for line in f:
        tab_split = line.split('\t') # 7 tab delimited sections 


        english_word = tab_split[1] 

        german_word = tab_split[4]
        part_of_speech = tab_split[2]


        en_to_de[Vertex(english_word, part_of_speech, english)
                     ].append(Vertex(german_word, part_of_speech, german))

        de_to_en[Vertex(german_word, part_of_speech, german)
                ].append(Vertex(english_word, part_of_speech, english))





    
