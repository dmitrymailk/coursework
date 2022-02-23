from text_popularity import TextPopularity
from grammar_text_analysis import TextAnalysis
import os
from progress.bar import ChargingBar
from natsort import natsorted, ns
import pickle


class ScoreText:
    def __init__(self, rawtext):
        w = 0.55
        weights = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1, 0.1, 0.5, 0.5, 0.5, 0.1, 0.1, 0.1, 0.5, 0.5,
                   0.1, 0.5, 0.1, 0.5, 0.5, 0.5, 0.1, 0.1, 1, 2, 2, 3, 0.5, 1, 0.5, 4, 3, 4, 5, 5, 3, 2, 1]
        weights = [num * w for num in weights]
        self.rawtext = rawtext
        self.voc = TextPopularity(rawtext)
        self.gram = TextAnalysis(rawtext, weights)
        self.score = self.voc.score + self.gram.score


# test = ScoreText(open("one-text.txt").read())

# print(
#     f"\nScore {test.score}\nGrammar {test.gram.score}\nWords {test.voc.score}")
