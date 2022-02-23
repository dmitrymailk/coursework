import spacy
from nltk.corpus import stopwords

nlp = spacy.load('en_core_web_lg')
nlp.max_length = 10 ** 50


class TextPopularity:
    def __init__(self, rawtext):
        # self.filename = filename
        self.rawtext = str(rawtext)
        self.score = 0

        self.average_score_pop()

    def average_score_pop(self):
        corpuses = ['ted-talks-counts.txt', 'reddit-counts-1.txt', ]

        scores = []

        for corpus in corpuses:
            score = self.score_pop(corpus, self.rawtext, 3000)
            scores.append(score)
        self.score = (scores[0] + scores[1]) / 2
        # print(f"Words score {self.filename} = {self.popularity}")

    def score_pop(self, corpusname, rawtext, count_top):
        word_counts = open(corpusname, encoding="utf-8")
        top_words = []

        for i in range(count_top):
            line = word_counts.readline()
            hyp_index = 0
            word = ''
            if '-' in line:
                hyp_index = line.index('-')
                word = line[:hyp_index].strip()
            else:
                word = line.strip()
            if len(word) > 0:
                top_words.append(word)

        # random_text = open(filename, 'r', encoding='utf-8').read()
        test_message = nlp(rawtext)

        stop_words = set(stopwords.words('english'))

        words_in_test = set([str(item.lemma_).lower() for item in test_message if str(
            item.lemma_).isalpha() and not str(item.lemma_).lower() in stop_words])

        diff_words = set(words_in_test) - set(top_words)
        # print( len(words_in_test) , len(diff_words))

        # print(f'Text popularity for corpus {corpusname} = {(len(words_in_test) - len(diff_words)) / len(words_in_test)}')

        return round(len(diff_words) / len(words_in_test) * 100)
