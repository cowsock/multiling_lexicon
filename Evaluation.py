# -*- coding: utf-8 -*-
from __future__ import division

import argparse

import io

from collections import defaultdict

from Util import Vertex


class Sent_Entry(object):
    """convenience struct for readability.
       Represents data from German sentiment lexicon source"""
    def __init__(self, feature_, lemma_, pos_, polarity_, probability_):
        self.feature = feature_
        self.lemma = lemma_
        self.pos = pos_ 
        self.polarity = polarity_
        self.probability = probability_


def parse_sent_file(f):
    for line in f:
        temp = line.split("\t")
        yield Sent_Entry(temp[0], temp[1], temp[2], temp[3], temp[4])

def get_entries_set(filename):
    entries = set()
    with io.open(filename, encoding="utf-8") as f:
        for entry in parse_sent_file(f):
            # should use vertex format
            entries.add(Vertex(entry.feature, entry.pos, "DE"))
            entries.add(Vertex(entry.lemma, entry.pos, "DE"))
    return entries

def eval_collection(prediction, gold):
    intersect = prediction & gold
    tp = len(intersect)
    print "Total True Positive: {0}".format(tp)
    
    fn = len(gold) - tp

    fp = len(prediction) - tp

    pre = precision(tp, fp)
    rec = recall(tp, fn)

    f_score = f1(pre, rec)

    print "Precision: {0}\nRecall: {1}\nF1: {2}".format(pre, rec, f_score)


def precision(tp, fp):
    assert tp >= 0
    assert fp >= 0
    if (tp + fp) == 0:
        return 0
    return tp / (tp + fp)

def recall(tp, fn):
    assert tp >= 0
    assert fn >= 0
    if (tp + fn) == 0:
        return 0
    return tp / (tp + fn)

def f1(pre, rec):
    if (pre + rec) == 0:
        return 0
    return 2 * ((pre * rec) / (pre + rec))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluates stats of German sentiment lexicon")
    parser.add_argument("de_sent_lex_file", type=str, help="input file containing a german sentiment lexicon to be evaluated against a gold standard")

    args = parser.parse_args()

    positive_predictions = set()
    negative_predictions = set()
    neutral_predictions = set()

    with io.open(args.de_sent_lex_file, encoding='utf-8') as f:
        for line in f:
            temp = line.split('\t')
            v = Vertex(temp[0], temp[1], temp[2])
            if temp[3] == "Positive\n":
                positive_predictions.add(v)
            elif temp[3] == "Negative\n":
                negative_predictions.add(v)
            elif temp[3] == "Neutral\n":
                neutral_predictions.add(v)
            else:
                assert False


    # ok so that needs to be a readable file

    # also need to parse the gold standard file

    gold_directory = "GermanPolarityClues-2012/"

    gold_positive = gold_directory + "GermanPolarityClues-Positive-Lemma-21042012.tsv"

    gold_negative = gold_directory + "GermanPolarityClues-Negative-Lemma-21042012.tsv"



    all_predicted = positive_predictions | negative_predictions 

    # need to constrain gold set by things that are actually contained in the predictions set

    positive_entries = get_entries_set(gold_positive) 

    negative_entries = get_entries_set(gold_negative) 



    # now that we have all of the ingredients, check how well we did

   


    print "Positive"
    print "Total classified: {0}".format(len(positive_predictions))
    eval_collection(positive_predictions, positive_entries)
    print "\nNegative"
    print "Total classified: {0}".format(len(negative_predictions))
    eval_collection(negative_predictions, negative_entries)



