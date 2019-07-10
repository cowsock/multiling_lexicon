# -*- coding: utf-8 -*-

noun = "noun"
verb = "verb"
adj = "adj"
adv = "adv"

german = "DE"

english = "EN"

POS_CONVERSION = {"ADJ":adj, "NN":noun, "V":verb, # from germanet
                  "a":adj, "n":noun, "s":adj, "r":adv, "v":verb, # from wordnet
                  "adv":adv, "adj":adj, "verb":verb, "noun":noun, # from dict.cc
                  "VV":verb, "AD":adj, "VM":verb} # from german sent lexicon


def convert_pos(pos):
    try:
        return POS_CONVERSION[pos]
    except KeyError:
        return "UNKNOWN"

class Vertex(object):
    def __init__(self, w_, pos_, lang_):
        self.w = w_
        self.pos = convert_pos(pos_)
        self.lang = lang_

    def __eq__(self, other):
        return self.w == other.w and \
               self.pos == other.pos and self.lang == other.lang

    def __hash__(self):
        return hash(self.w) ^ hash(self.pos) ^ hash(self.lang)

    def __unicode__(self):
        return u"{0} ({1})".format(self.w, self.pos)

    def __repr__(self):
        return "{0} ({1})".format(self.w.encode("utf-8"), self.pos)


# POS tags should be converted "on arrival" so that the confusing mess
# that is having a different stardard in every file is averted