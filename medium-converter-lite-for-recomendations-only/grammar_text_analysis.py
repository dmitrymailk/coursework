import spacy
from spacy.matcher import Matcher
from progress.bar import ChargingBar

nlp = spacy.load("en_core_web_lg")
nlp.max_length = 10 ** 50

w = 0.55
weights = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1, 0.1, 0.5, 0.5, 0.5, 0.1, 0.1, 0.1, 0.5, 0.5,
           0.1, 0.5, 0.1, 0.5, 0.5, 0.5, 0.1, 0.1, 1, 2, 2, 3, 0.5, 1, 0.5, 4, 3, 4, 5, 5, 3, 2, 1]

weights = [num * w for num in weights]


class TextAnalysis:
    def __init__(self, rawtext, weights=weights):
        # self.filename = filename
        # self.source = open(filename, 'r', encoding='utf-8').read()
        self.rawtext = rawtext
        self.text = nlp(self.rawtext)
        self.sents = [sent for sent in self.text.sents]
        self.score = 0
        self.all_functions = [
            # 1
            self.adjectives_demonstrative,
            # 2
            self.adverbs_of_frequency,
            # 3
            self.comparatives_and_superlatives,
            # 4
            self.going_to,
            # 5
            self.how_much_many,
            # 6
            self.would_like,
            # 7
            self.imperatives,
            # 8
            self.intensifiers,
            # 9
            self.modals,
            # 10
            self.past_simple_to_be,
            # 11
            self.past_simple,
            # 12
            self.possessive_adjectives,
            # 13
            self.possessive_s,
            # 14
            self.prepositions_common,
            # 15
            self.prepositions_of_place,
            # 16
            self.prepositions_of_time,
            # 17
            self.present_continuous,
            # 18
            self.present_simple,
            # 19
            self.pronouns_simple_personal,
            # 20
            self.there_is_are,
            # 21
            self.verb_be,
            # 22
            self.verb_ing_like_hate_love,
            # 23
            self.than_and_definite,
            # 24
            self.adjectives_superlative_definite,
            # 25
            self.adverbial_time_place_and_frequency,
            # 26
            self.much_many,
            # 27
            self.future_time,
            # 28
            self.past_continuous,
            # 29
            self.present_perfect,
            # 30
            self.future_continuous,
            # 31
            self.questions,
            # 32
            self.gerunds,
            # 33
            self.connecting_words,
            # 34
            self.past_perfect,
            # 35
            self.present_perfect_continuous,
            # 36
            self.future_perfect_continuous,
            # 37
            self.past_perfect_continuous,
            # 38
            self.future_perfect,
            # 39
            self.simple_passive,
            # 40
            self.perfect_modals,
            # 41
            self.expressing_habits,
        ]
        self.sents_length = len(self.sents)
        self.len_all_func = 0
        self.weights_array = weights
        # Count occurenses
        self.adjectives_demonstrative_count = 0
        self.adverbs_of_frequency_count = 0
        self.comparatives_and_superlatives_count = 0
        self.going_to_count = 0
        self.how_much_many_count = 0
        self.would_like_count = 0
        self.imperatives_count = 0
        self.intensifiers_count = 0
        self.modals_count = 0
        self.past_simple_to_be_count = 0
        self.past_simple_count = 0
        self.possessive_adjectives_count = 0
        self.possessive_s_count = 0
        self.prepositions_common_count = 0
        self.prepositions_of_place_count = 0
        self.prepositions_of_time_count = 0
        self.present_continuous_count = 0
        self.present_simple_count = 0
        self.pronouns_simple_personal_count = 0
        self.there_is_are_count = 0
        self.verb_be_count = 0
        self.verb_ing_like_hate_love_count = 0
        self.than_and_definite_count = 0
        self.adjectives_superlative_definite_count = 0
        self.adverbial_time_place_and_frequency_count = 0
        self.much_many_count = 0
        self.future_time_count = 0
        self.past_continuous_count = 0
        self.present_perfect_count = 0
        self.future_continuous_count = 0
        self.questions_count = 0
        self.gerunds_count = 0
        self.connecting_words_count = 0
        self.past_perfect_count = 0
        self.present_perfect_continuous_count = 0
        self.future_perfect_continuous_count = 0
        self.past_perfect_continuous_count = 0
        self.future_perfect_count = 0
        self.simple_passive_count = 0
        self.perfect_modals_count = 0
        self.expressing_habits_count = 0

        # START DEFAULT ANALYSIS
        if len(self.all_functions) == len(self.weights_array):
            # print('start analysis')
            self.text_analysis()
        else:
            print(
                f"incorrect length func = {len(self.all_functions)} and weights = {len(self.weights_array)}")

    def analysis_sent(self, sent):
        sent = str(sent)

        self.len_all_func = len(self.all_functions)

        for i in range(len(self.all_functions)):
            func_count = f"{self.all_functions[i].__name__}_count"
            if getattr(self, func_count) < 5:
                res_sent_analysis = self.all_functions[i](sent)
                if res_sent_analysis:
                    count = getattr(self, func_count)
                    count += 1
                    setattr(self, func_count, count)
                    weight = self.weights_array[i]
                    self.score += weight

    def text_analysis(self):
        # start main process
        length = len(self.sents)

        for sent in self.sents:
            self.analysis_sent(str(sent))

        # print()
        # print(f'Grammar score {self.filename} = {self.score}')

    def full_text_analysis(self, filename):
        final_str = ""
        file_sents = open(filename, 'w', encoding="utf-8")

        for sent in self.sents:
            final_str += self.analysis_sent_full(str(sent))

        file_sents.write(final_str)

        count_all_grammar = ""

        for i in range(len(self.all_functions)):
            name_func = f"{self.all_functions[i].__name__}_count"
            count_all_grammar += f"{self.all_functions[i].__name__:15} --- {getattr(self,name_func)}\n"

        file_sents.write(count_all_grammar)
        file_sents.close()

        print("all sents done!")

    def increase_score(self, state, points):
        if state:
            self.score += points
# 1 self.increase_score()

    def adjectives_demonstrative(self, sent):
        sent = [str(token).lower() for token in nlp(sent)]
        adjectives_list = ['here', "this", "these", "there", "that", "those"]
        has_adjective = False
        for word in sent:
            if word in adjectives_list:
                has_adjective = True
                break

        return has_adjective
# 2

    def adverbs_of_frequency(self, sent):
        sent = [str(token).lower() for token in nlp(sent)]
        adverbs_list = ['always', 'frequently', 'generally', 'hardly ever', 'infrequently', 'never',
                        'normally', 'occasionally', 'often', 'rarely', 'regularly', 'seldom', 'sometimes', 'usually',
                        'once in a while', 'every now and again', 'from time to time']
        has_adverb = False
        for word in sent:
            if word in adverbs_list:
                has_adverb = True
                break

        return has_adverb
# 3

    def comparatives_and_superlatives(self, sent):
        matcher = Matcher(nlp.vocab)

        pattern_1 = [{'TAG': 'JJR'}]
        pattern_2 = [{'TAG': 'JJS'}]
        pattern_3 = [{'TEXT': 'most'}, {'TAG': 'JJ'}]
        pattern_4 = [{'TEXT': 'more'}, {'TAG': 'JJ'}]
        pattern_5 = [{'TAG': 'RBR'}]
        pattern_6 = [{'TAG': 'RBS'}]

        matcher.add('comparatives_and_superlatives', None, pattern_1,
                    pattern_2, pattern_3, pattern_4, pattern_5, pattern_6)

        sent = nlp(sent)
        matches = matcher(sent)
        phrase = ''

        # for token in sent:
        #   print(token.text, token.pos_, token.tag_)

        for match_id, start, end in matches:
            span = sent[start:end]
            phrase = span.text
            # print(phrase)

        if len(phrase) > 0:
            return phrase
        else:
            return False
# 4

    def going_to(self, sent):
        has_going = False

        if 'going to' in str(sent).lower():
            has_going = True

        return has_going
# 5

    def how_much_many(self, sent):
        has_much_many = False

        if 'how much' in sent.lower():
            has_much_many = True

        if 'how many' in sent.lower():
            has_much_many = True

        return has_much_many
# 6

    def would_like(self, sent):
        has_would_like = False

        if "'d like" in sent.lower():
            has_would_like = True

        if "'d not like" in sent.lower():
            has_would_like = True

        if "’d like" in sent.lower():
            has_would_like = True

        if "’d not like" in sent.lower():
            has_would_like = True

        if 'would like' in sent.lower():
            has_would_like = True

        if 'would not like' in sent.lower():
            has_would_like = True

        if "wouldn't like" in sent.lower():
            has_would_like = True

        matcher = Matcher(nlp.vocab)

        pattern_1 = [{'TAG': 'MD'}, {'TAG': 'PRP'}, {'TAG': 'VB'}]

        matcher.add('would_like', None, pattern_1)

        sent = nlp(sent)
        matches = matcher(sent)
        # print(sent)
        # for token in sent:
        #   print(token.text, token.pos_, token.tag_)

        for match_id, start, end in matches:
            has_would_like = True
            break

        return has_would_like
# 7

    def imperatives(self, sent):
        has_imperatives = False
        if nlp(str(sent))[0].tag_ == "VB" or str(sent)[-1] == "!" or str(sent).split()[0].lower() in ['always', 'never', 'often', 'seldom', 'sometimes', 'usually', 'please']:
            has_imperatives = True

        return has_imperatives
# 8

    def intensifiers(self, sent):
        phrase = ''
        matcher = Matcher(nlp.vocab)

        pattern_1 = [{'TEXT': 'very'}, {'TAG': 'JJ'}]
        pattern_2 = [{'TEXT': 'very'}, {'TAG': 'RB'}]
        pattern_3 = [{'TEXT': 'really'}, {'TAG': 'JJ'}]
        pattern_4 = [{'TEXT': 'extremely'}, {'TAG': 'JJ'}]
        pattern_5 = [{'TEXT': 'so'}, {'TAG': 'JJ'}]
        pattern_6 = [{'TEXT': 'so'}, {'TAG': 'RB'}]
        pattern_7 = [{'TEXT': 'too'}, {'TAG': 'RB'}]
        pattern_8 = [{'TAG': 'RB'}, {'TEXT': 'enough'}]
        pattern_9 = [{'TAG': 'JJ'}, {'TEXT': 'enough'}]

        matcher.add('intensifiers', None, pattern_1, pattern_2, pattern_3,
                    pattern_4, pattern_5, pattern_6,
                    pattern_7, pattern_8, pattern_9)

        sent = nlp(sent)
        matches = matcher(sent)
        # print(sent)
        # for token in sent:
        #   print(token.text, token.pos_, token.tag_)

        for match_id, start, end in matches:
            span = sent[start:end]
            phrase = span.text.lower()

        if len(phrase) > 0:
            return phrase
        else:
            return False
# 9

    def modals(self, sent):
        # perfomance issues
        has_modals = False
        sent = sent.lower()
        # sent = [str(token).lower() for token in nlp(sent)]
        modals_list = ['can', 'could', 'may', 'might', 'will',
                       'would', 'shall', 'should', 'must', 'have to', 'has to']
        for word in modals_list:
            if word in sent:
                has_modals = True
                break

        return has_modals
# 10

    def past_simple_to_be(self, sent):
        phrase = ''
        matcher = Matcher(nlp.vocab)

        pattern_1 = [{'TAG': 'NN'}, {'TEXT': 'was'},
                     {'POS': "VERB", "OP": "!"}]
        pattern_2 = [{'TAG': 'NN'}, {'TEXT': 'were'},
                     {'POS': "VERB", "OP": "!"}]
        pattern_3 = [{'TAG': 'NN'}, {'TEXT': 'was not'}, ]
        pattern_4 = [{'TAG': 'NN'}, {'TEXT': 'were not'}, ]
        pattern_5 = [{'TEXT': 'was'}, {'TAG': 'NN'}, ]
        pattern_6 = [{'TEXT': 'were'}, {'TAG': 'NN'}, ]
        pattern_7 = [{'TEXT': 'was not'}, {'TAG': 'NN'}, ]
        pattern_8 = [{'TEXT': 'were not'}, {'TAG': 'NN'}, ]
        pattern_9 = [{'POS': 'PRON'}, {'TEXT': 'were'},
                     {'POS': "VERB", "OP": "!"}]
        pattern_10 = [{'POS': 'PRON'}, {
            'TEXT': 'was'}, {'POS': "VERB", "OP": "!"}]
        pattern_11 = [{'TEXT': 'was not'}, {'POS': 'PRON'}, ]
        pattern_12 = [{'TEXT': 'were not'}, {'POS': 'PRON'}]

        matcher.add('past_simple_to_be', None, pattern_1, pattern_2, pattern_3,
                    pattern_4, pattern_5, pattern_6,
                    pattern_7, pattern_8, pattern_9,
                    pattern_10, pattern_11, pattern_12)

        sent = nlp(sent.lower())
        matches = matcher(sent)
        # print(sent)
        # for token in sent:
        #   print(token.text, token.pos_, token.tag_)

        for match_id, start, end in matches:
            span = sent[start:end]
            phrase = span.text.replace('.', '')
            if len(phrase.split()) > 2:
                phrase = " ".join(phrase.split()[:2])
            # if len(phrase.split()) > 2 and phrase.split()[1] == 'not':
            #   phrase = " ".join(phrase.split())
            # print(phrase)

        if len(phrase) > 0:
            return phrase
        else:
            return False
# 11

    def past_simple(self, sent):
        phrase = ''
        matcher = Matcher(nlp.vocab)

        pattern_1 = [{'TAG': 'PRP'}, {'TAG': 'VBD'}]
        pattern_2 = [{'TAG': 'NN'}, {'TAG': 'VBD'}]
        pattern_3 = [{'TAG': 'NNS'}, {'TAG': 'VBD'}]
        pattern_4 = [{'TAG': 'NNP'}, {'TAG': 'VBD'}]
        pattern_5 = [{'TAG': 'NNPS'}, {'TAG': 'VBD'}]

        pattern_6 = [{"TEXT": "did"}, {'TAG': 'PRP'}, {'TAG': 'VB'}]
        pattern_7 = [{"TEXT": "did"}, {'TAG': 'NN'}, {'TAG': 'VB'}]
        pattern_8 = [{"TEXT": "did"}, {'TAG': 'NNP'}, {'TAG': 'VB'}]
        pattern_9 = [{"TEXT": "did"}, {'TAG': 'NNPS '}, {'TAG': 'VB'}]

        pattern_10 = [{"TAG": "VBD"}, {"TEXT": "not"},
                      {'TAG': 'PRP'}, {'TAG': 'VB'}]
        pattern_11 = [{"TAG": "VBD"}, {"TEXT": "not"},
                      {'TAG': 'NN'}, {'TAG': 'VB'}]
        pattern_12 = [{"TAG": "VBD"}, {"TEXT": "not"},
                      {'TAG': 'NNP'}, {'TAG': 'VB'}]
        pattern_13 = [{"TAG": "VBD"}, {"TEXT": "not"},
                      {'TAG': 'NNPS '}, {'TAG': 'VB'}]

        pattern_14 = [{"TEXT": "who"}, {'TAG': 'VBD'}, ]

        matcher.add('past_simple', None, pattern_1, pattern_2, pattern_3,
                    pattern_4, pattern_5, pattern_6,
                    pattern_7, pattern_8, pattern_9,
                    pattern_10, pattern_11, pattern_12,
                    pattern_13, pattern_14)

        sent = nlp(sent.lower())
        matches = matcher(sent)
        # print(sent)
        # for token in sent:
        #   print(token.text, token.pos_, token.tag_)

        for match_id, start, end in matches:
            span = sent[start:end]
            phrase = span.text
            # if len(phrase.split()) > 2 and phrase.split()[1] == 'not':
            #   phrase = " ".join(phrase.split())
            # print(phrase)

        if len(phrase) > 0:
            return phrase
        else:
            return False
# 12

    def possessive_adjectives(self, sent):
        has_possessive_adjectives = False
        possessive_adjectives_list = [
            'my', 'your', 'his', 'her', '	its', 'our', 'their']
        sent = [str(token).lower() for token in nlp(sent)]
        for word in sent:
            if word in possessive_adjectives_list:
                has_possessive_adjectives = True
                break

        # self.increase_score(has_possessive_adjectives, 1)
        return has_possessive_adjectives
# 13

    def possessive_s(self, sent):
        has_possessive_s = False
        matcher = Matcher(nlp.vocab)

        pattern_1 = [{'TAG': 'POS'}]

        matcher.add('possessive_s', None, pattern_1)

        sent = nlp(sent.lower())
        matches = matcher(sent)

        # print(sent)
        # for token in sent:
        #   print(token.text, token.pos_, token.tag_)

        for match_id, start, end in matches:
            span = sent[start:end]
            has_possessive_s = True
            # print(phrase)
            # break

        return has_possessive_s
# 14

    def prepositions_common(self, sent):
        has_prepositions_common = False
        prepositions_common_list = ['at', 'by',
                                    'for', 'from', 'in', 'on', 'to', 'with']
        sent = [str(token).lower() for token in nlp(sent)]

        for word in sent:
            if word in prepositions_common_list:
                has_prepositions_common = True
                break

        return has_prepositions_common
# 15

    def prepositions_of_place(self, sent):
        has_prepositions_of_place = False
        prepositions_of_place_list = ['in', 'at', 'on', 'next to', 'near', 'by', 'between', 'behind', 'in front of', 'under',
                                      'below', 'over', 'above', 'across', 'through', 'to', 'into', 'towards', 'onto', 'from']
        sent = [str(token).lower() for token in nlp(sent)]

        for word in sent:
            if word in prepositions_of_place_list:
                has_prepositions_of_place = True
                break

        return has_prepositions_of_place
# 16

    def prepositions_of_time(self, sent):
        has_prepositions_of_time = False
        prepositions_of_time_list = [
            'on', 'in', 'at', 'since', 'for', 'ago', 'before', 'to', 'past', 'from', 'till', 'by']
        sent = [str(token).lower() for token in nlp(sent)]

        for word in sent:
            if word in prepositions_of_time_list:
                has_prepositions_of_time = True
                break

        return has_prepositions_of_time
# 17

    def present_continuous(self, sent):
        phrase = ''
        matcher = Matcher(nlp.vocab)

        pattern_1 = [{'TAG': 'NNP'}, {"TEXT": "am"}, {'TAG': 'VBG'}]
        pattern_2 = [{'TAG': 'NNPS'}, {"TEXT": "am"}, {'TAG': 'VBG'}]
        pattern_3 = [{'TAG': 'NN'}, {"TEXT": "am"}, {'TAG': 'VBG'}]
        pattern_4 = [{'TAG': 'PRP'}, {"TEXT": "am"}, {'TAG': 'VBG'}]

        pattern_5 = [{'TAG': 'NNP'}, {"TEXT": "is"}, {'TAG': 'VBG'}]
        pattern_6 = [{'TAG': 'NNPS'}, {"TEXT": "is"}, {'TAG': 'VBG'}]
        pattern_7 = [{'TAG': 'NN'}, {"TEXT": "is"}, {'TAG': 'VBG'}]
        pattern_8 = [{'TAG': 'PRP'}, {"TEXT": "is"}, {'TAG': 'VBG'}]

        pattern_9 = [{'TAG': 'NNP'}, {"TEXT": "are"}, {'TAG': 'VBG'}]
        pattern_10 = [{'TAG': 'NNPS'}, {"TEXT": "are"}, {'TAG': 'VBG'}]
        pattern_11 = [{'TAG': 'NN'}, {"TEXT": "are"}, {'TAG': 'VBG'}]
        pattern_12 = [{'TAG': 'PRP'}, {"TEXT": "are"}, {'TAG': 'VBG'}]

        pattern_13 = [{"TEXT": "am"}, {'TAG': 'NNP'}, {'TAG': 'VBG'}]
        pattern_14 = [{"TEXT": "am"}, {'TAG': 'NNPS'}, {'TAG': 'VBG'}]
        pattern_15 = [{"TEXT": "am"}, {'TAG': 'NN'}, {'TAG': 'VBG'}]
        pattern_16 = [{"TEXT": "am"}, {'TAG': 'PRP'}, {'TAG': 'VBG'}]

        pattern_17 = [{"TEXT": "is"}, {'TAG': 'NNP'}, {'TAG': 'VBG'}]
        pattern_18 = [{"TEXT": "is"}, {'TAG': 'NNPS'}, {'TAG': 'VBG'}]
        pattern_19 = [{"TEXT": "is"}, {'TAG': 'NN'}, {'TAG': 'VBG'}]
        pattern_20 = [{"TEXT": "is"}, {'TAG': 'PRP'}, {'TAG': 'VBG'}]

        pattern_21 = [{"TEXT": "are"}, {'TAG': 'NNP'}, {'TAG': 'VBG'}]
        pattern_22 = [{"TEXT": "are"}, {'TAG': 'NNPS'}, {'TAG': 'VBG'}]
        pattern_23 = [{"TEXT": "are"}, {'TAG': 'NN'}, {'TAG': 'VBG'}]
        pattern_24 = [{"TEXT": "are"}, {'TAG': 'PRP'}, {'TAG': 'VBG'}]

        pattern_25 = [{'TAG': 'NNP'}, {"TAG": "VBP"},
                      {"TEXT": "not"}, {'TAG': 'VBG'}]
        pattern_26 = [{'TAG': 'NNPS'}, {"TAG": "VBP"},
                      {"TEXT": "not"}, {'TAG': 'VBG'}]
        pattern_27 = [{'TAG': 'NN'}, {"TAG": "VBP"},
                      {"TEXT": "not"}, {'TAG': 'VBG'}]
        pattern_28 = [{'POS': 'PRON'}, {"TAG": "VBP"},
                      {"TEXT": "not"}, {'TAG': 'VBG'}]

        pattern_29 = [{'TAG': 'NNP'}, {"TAG": "VBZ"},
                      {"TEXT": "not"}, {'TAG': 'VBG'}]
        pattern_30 = [{'TAG': 'NNPS'}, {"TAG": "VBZ"},
                      {"TEXT": "not"}, {'TAG': 'VBG'}]
        pattern_31 = [{'TAG': 'NN'}, {"TAG": "VBZ"},
                      {"TEXT": "not"}, {'TAG': 'VBG'}]
        pattern_32 = [{'TAG': 'PRP'}, {"TAG": "VBZ"},
                      {"TEXT": "not"}, {'TAG': 'VBG'}]

        pattern_33 = [{'TAG': 'NNP'}, {"TEXT": "are not"}, {'TAG': 'VBG'}]
        pattern_34 = [{'TAG': 'NNPS'}, {"TEXT": "are not"}, {'TAG': 'VBG'}]
        pattern_35 = [{'TAG': 'NN'}, {"TEXT": "are not"}, {'TAG': 'VBG'}]
        pattern_36 = [{'TAG': 'PRP'}, {"TEXT": "are not"}, {'TAG': 'VBG'}]

        matcher.add('present_continuous', None,
                    pattern_1, pattern_2, pattern_3, pattern_4,
                    pattern_5, pattern_6, pattern_7, pattern_8,
                    pattern_9, pattern_10, pattern_11, pattern_12,
                    pattern_13, pattern_14, pattern_15, pattern_16,
                    pattern_17, pattern_18, pattern_19, pattern_20,
                    pattern_21, pattern_22, pattern_23, pattern_24,
                    pattern_25, pattern_26, pattern_27, pattern_28,
                    pattern_29, pattern_30, pattern_31, pattern_32,
                    pattern_33, pattern_34, pattern_35, pattern_36,)

        sent = nlp(sent.lower())
        matches = matcher(sent)
        # print(sent)
        # for token in sent:
        #   print(token.text, token.pos_, token.tag_)

        for match_id, start, end in matches:
            span = sent[start:end]
            phrase = span.text
            # if len(phrase.split()) > 2 and phrase.split()[1] == 'not':
            #   phrase = " ".join(phrase.split())
            # print(phrase)

        if len(phrase) > 0:
            return phrase
        else:
            return False
# 18

    def present_simple(self, sent):
        phrase = ''
        matcher = Matcher(nlp.vocab)

        pattern_1 = [{'TAG': 'NN'}, {'TAG': 'VBP'}]
        pattern_2 = [{'TAG': 'NNS'}, {'TAG': 'VBP'}]
        pattern_3 = [{'TAG': 'NNP'}, {'TAG': 'VBP'}]
        pattern_4 = [{'TAG': 'NNPS'}, {'TAG': 'VBP'}]
        pattern_5 = [{'TAG': 'PRP'}, {'TAG': 'VBP'}]

        pattern_6 = [{'TAG': 'NN'}, {'TAG': 'VBZ'}]
        pattern_7 = [{'TAG': 'NNS'}, {'TAG': 'VBZ'}]
        pattern_8 = [{'TAG': 'NNP'}, {'TAG': 'VBZ'}]
        pattern_9 = [{'TAG': 'NNPS'}, {'TAG': 'VBZ'}]
        pattern_10 = [{'TAG': 'PRP'}, {'TAG': 'VBZ'}]

        pattern_11 = [{"TEXT": "do"}, {'TAG': 'NN'}, {'TAG': 'VBP'}]
        pattern_12 = [{"TEXT": "do"}, {'TAG': 'NNS'}, {'TAG': 'VBP'}]
        pattern_13 = [{"TEXT": "do"}, {'TAG': 'NNP'}, {'TAG': 'VBP'}]
        pattern_14 = [{"TEXT": "do"}, {'TAG': 'NNPS'}, {'TAG': 'VBP'}]
        pattern_15 = [{"TEXT": "do"}, {'TAG': 'PRP'}, {'TAG': 'VBP'}]

        pattern_16 = [{"TEXT": "do"}, {'TAG': 'NN'}, {'TAG': 'VB'}]
        pattern_17 = [{"TEXT": "do"}, {'TAG': 'NNS'}, {'TAG': 'VB'}]
        pattern_18 = [{"TEXT": "do"}, {'TAG': 'NNP'}, {'TAG': 'VB'}]
        pattern_19 = [{"TEXT": "do"}, {'TAG': 'NNPS'}, {'TAG': 'VB'}]
        pattern_20 = [{"TEXT": "do"}, {'TAG': 'PRP'}, {'TAG': 'VB'}]

        pattern_21 = [{"TEXT": "does"}, {'TAG': 'NN'}, {'TAG': 'VBP'}]
        pattern_22 = [{"TEXT": "does"}, {'TAG': 'NNS'}, {'TAG': 'VBP'}]
        pattern_23 = [{"TEXT": "does"}, {'TAG': 'NNP'}, {'TAG': 'VBP'}]
        pattern_24 = [{"TEXT": "does"}, {'TAG': 'NNPS'}, {'TAG': 'VBP'}]
        pattern_25 = [{"TEXT": "does"}, {'TAG': 'PRP'}, {'TAG': 'VBP'}]

        pattern_26 = [{"TEXT": "does"}, {'TAG': 'NN'}, {'TAG': 'VB'}]
        pattern_27 = [{"TEXT": "does"}, {'TAG': 'NNS'}, {'TAG': 'VB'}]
        pattern_28 = [{"TEXT": "does"}, {'TAG': 'NNP'}, {'TAG': 'VB'}]
        pattern_29 = [{"TEXT": "does"}, {'TAG': 'NNPS'}, {'TAG': 'VB'}]
        pattern_30 = [{"TEXT": "does"}, {'TAG': 'PRP'}, {'TAG': 'VB'}]

        # with adverbs
        pattern_31 = [{'TAG': 'NN'}, {"TAG": "RB"}, {'TAG': 'VBP'}]
        pattern_32 = [{'TAG': 'NNS'}, {"TAG": "RB"}, {'TAG': 'VBP'}]
        pattern_33 = [{'TAG': 'NNP'}, {"TAG": "RB"}, {'TAG': 'VBP'}]
        pattern_34 = [{'TAG': 'NNPS'}, {"TAG": "RB"}, {'TAG': 'VBP'}]
        pattern_35 = [{'TAG': 'PRP'}, {"TAG": "RB"}, {'TAG': 'VBP'}]

        pattern_36 = [{'TAG': 'NN'}, {"TAG": "RB"}, {'TAG': 'VBZ'}]
        pattern_37 = [{'TAG': 'NNS'}, {"TAG": "RB"}, {'TAG': 'VBZ'}]
        pattern_38 = [{'TAG': 'NNP'}, {"TAG": "RB"}, {'TAG': 'VBZ'}]
        pattern_39 = [{'TAG': 'NNPS'}, {"TAG": "RB"}, {'TAG': 'VBZ'}]
        pattern_40 = [{'TAG': 'PRP'}, {"TAG": "RB"}, {'TAG': 'VBZ'}]

        matcher.add('present_simple', None,
                    pattern_1, pattern_2, pattern_3,
                    pattern_4, pattern_5, pattern_6,
                    pattern_7, pattern_8, pattern_9,
                    pattern_10, pattern_11, pattern_12,
                    pattern_13, pattern_14, pattern_15,
                    pattern_16, pattern_17, pattern_18,
                    pattern_19, pattern_20, pattern_21,
                    pattern_22, pattern_23, pattern_24,
                    pattern_25, pattern_26, pattern_27,
                    pattern_28, pattern_29, pattern_30,
                    pattern_31,
                    pattern_32, pattern_33, pattern_34,
                    pattern_35, pattern_36, pattern_37,
                    pattern_38, pattern_39, pattern_40,)

        sent = nlp(sent.lower())
        matches = matcher(sent)
        # print(sent)
        # for token in sent:
        #   print(token.text, token.pos_, token.tag_)

        for match_id, start, end in matches:
            span = sent[start:end]
            phrase = span.text
            # print(phrase)

        # DUMB FIX

        phrase = phrase.replace('i am', '')

        if len(phrase) > 0:
            return phrase
        else:
            return False
# 19

    def pronouns_simple_personal(self, sent):
        has_pronouns_simple_personal = False
        pronouns_simple_personal_list = [
            'me', 'him', 'her', 'it', 'us', 'you', 'them', ]

        sent = [str(token).lower() for token in nlp(sent)]
        for word in sent:
            if word in pronouns_simple_personal_list:
                has_pronouns_simple_personal = True
                break

        return has_pronouns_simple_personal
# 20

    def there_is_are(self, sent):
        has_there_is_are = False
        there_is_are_list = ['there']

        sent = [str(token).lower() for token in nlp(sent)]
        for word in sent:
            if word in there_is_are_list:
                has_there_is_are = True
                break

        return has_there_is_are
# 21

    def verb_be(self, sent):
        has_verb_be = False
        verb_be_list = ['is', 'are', 'am', 'been',
                        'being', 'be', 'was', 'were', 'that']

        sent = [str(token).lower() for token in nlp(sent)]
        for word in sent:
            if word in verb_be_list:
                has_verb_be = True
                break

        return has_verb_be
# 22

    def verb_ing_like_hate_love(self, sent):
        phrase = ''
        matcher = Matcher(nlp.vocab)

        pattern_1 = [{'TEXT': 'love'}, {'TAG': 'VBG'}]
        pattern_2 = [{'TEXT': 'hate'}, {'TAG': 'VBG'}]
        pattern_3 = [{'TEXT': 'like'}, {'TAG': 'VBG'}]
        pattern_4 = [{'TEXT': 'prefer'}, {'TAG': 'VBG'}]

        pattern_5 = [{'TEXT': 'loves'}, {'TAG': 'VBG'}]
        pattern_6 = [{'TEXT': 'hates'}, {'TAG': 'VBG'}]
        pattern_7 = [{'TEXT': 'likes'}, {'TAG': 'VBG'}]
        pattern_8 = [{'TEXT': 'prefers'}, {'TAG': 'VBG'}]

        matcher.add('verb_ing_like_hate_love', None,
                    pattern_1, pattern_2, pattern_3, pattern_4,
                    pattern_5, pattern_6, pattern_7, pattern_8,
                    )

        sent = nlp(sent.lower())
        matches = matcher(sent)
        # print(sent)
        # for token in sent:
        #   print(token.text, token.pos_, token.tag_)

        for match_id, start, end in matches:
            span = sent[start:end]
            phrase = span.text
            # if len(phrase.split()) > 2 and phrase.split()[1] == 'not':
            #   phrase = " ".join(phrase.split())
            # print(phrase)

        if len(phrase) > 0:
            return phrase
        else:
            return False
# 23

    def than_and_definite(self, sent):
        phrase = ''
        matcher = Matcher(nlp.vocab)

        pattern_1 = [{'TAG': 'JJR'}, {'TEXT': 'than'}, ]
        pattern_2 = [{'TEXT': 'the'}, {'TAG': 'JJR'}, ]

        matcher.add('than_and_definite', None,
                    pattern_1, pattern_2
                    )

        sent = nlp(sent.lower())
        matches = matcher(sent)
        # print(sent)
        # for token in sent:
        #   print(token.text, token.pos_, token.tag_)

        for match_id, start, end in matches:
            span = sent[start:end]
            phrase = span.text
            # if len(phrase.split()) > 2 and phrase.split()[1] == 'not':
            #   phrase = " ".join(phrase.split())
            # print(phrase)

        if len(phrase) > 0:
            return phrase
        else:
            return False
# 24

    def adjectives_superlative_definite(self, sent):
        phrase = ''
        matcher = Matcher(nlp.vocab)

        pattern_1 = [{'TEXT': 'the'}, {'TAG': 'JJS'}, ]
        pattern_2 = [{'TEXT': 'the'}, {"TAG": "RBS"}, {'TAG': 'JJ'}, ]

        matcher.add('adjectives_superlative_definite', None,
                    pattern_1, pattern_2
                    )

        sent = nlp(sent.lower())
        matches = matcher(sent)
        # print(sent)
        # for token in sent:
        #   print(token.text, token.pos_, token.tag_)

        for match_id, start, end in matches:
            span = sent[start:end]
            phrase = span.text
            # print(phrase)

        if len(phrase) > 0:
            return phrase
        else:
            return False
# 25

    def adverbial_time_place_and_frequency(self, sent):
        has_adverbial_time_place_and_frequency = False
        adverbial_time_place_and_frequency_list = [
            'every',
            'once', 'twice',  'all the time', 'tomorrow',
            'tonight', 'yesterday', 'nowadays', 'now', 'first of all', 'beforehand', 'soon',
            'afterwards', 'later', 'next', 'then', 'outside', 'inside', 'indoors', 'outdoors',
            'upstairs', 'downstairs', 'here', 'there', 'abroad', 'overseas']

        sent = [str(token).lower() for token in nlp(sent)]
        for word in sent:
            if word in adverbial_time_place_and_frequency_list:
                has_adverbial_time_place_and_frequency = True
                break

        return has_adverbial_time_place_and_frequency
# 26

    def much_many(self, sent):
        has_much_many = False

        if 'much' in sent.lower():
            has_much_many = True

        if 'many' in sent.lower():
            has_much_many = True

        return has_much_many
# 27

    def future_time(self, sent):
        phrase = ''
        matcher = Matcher(nlp.vocab)

        pattern_1 = [{'TAG': 'NN'}, {"TEXT": "will"}, {'TAG': 'VB'}]
        pattern_2 = [{'TAG': 'NNS'}, {"TEXT": "will"}, {'TAG': 'VB'}]
        pattern_3 = [{'TAG': 'NNP'}, {"TEXT": "will"}, {'TAG': 'VB'}]
        pattern_4 = [{'TAG': 'NNPS'}, {"TEXT": "will"}, {'TAG': 'VB'}]
        pattern_5 = [{'POS': 'PRON'}, {"TEXT": "will"}, {'TAG': 'VB'}]

        pattern_6 = [{"TEXT": "'ll"}, {'TAG': 'VB'}]
        pattern_7 = [{"TEXT": "'ll"}, {'TAG': 'VB'}]
        pattern_8 = [{"TEXT": "'ll"}, {'TAG': 'VB'}]
        pattern_9 = [{"TEXT": "'ll"}, {'TAG': 'VB'}]
        pattern_10 = [{"TEXT": "'ll"}, {'TAG': 'VB'}]

        pattern_11 = [{"TEXT": "will"}, {'TAG': 'NN'}, {'TAG': 'VB'}]
        pattern_12 = [{"TEXT": "will"}, {'TAG': 'NNS'}, {'TAG': 'VB'}]
        pattern_13 = [{"TEXT": "will"}, {'TAG': 'NNP'}, {'TAG': 'VB'}]
        pattern_14 = [{"TEXT": "will"}, {'TAG': 'NNPS'}, {'TAG': 'VB'}]
        pattern_15 = [{"TEXT": "will"}, {'POS': 'PRON'}, {'TAG': 'VB'}]

        pattern_16 = [{"TAG": "MD"}, {"TEXT": "not"}, {'TAG': 'VB'}]
        pattern_17 = [{"TAG": "MD"}, {"TEXT": "not"}, {'TAG': 'VB'}]
        pattern_18 = [{"TAG": "MD"}, {"TEXT": "not"}, {'TAG': 'VB'}]
        pattern_19 = [{"TAG": "MD"}, {"TEXT": "not"}, {'TAG': 'VB'}]
        pattern_20 = [{"TAG": "MD"}, {"TEXT": "not"}, {'TAG': 'VB'}]

        matcher.add('future_time', None,
                    pattern_1, pattern_2, pattern_3, pattern_4, pattern_5,
                    pattern_6, pattern_7, pattern_8, pattern_9, pattern_10,
                    pattern_11, pattern_12, pattern_13, pattern_14, pattern_15,
                    pattern_16, pattern_17, pattern_18, pattern_19, pattern_20, )

        sent = nlp(sent.lower())
        matches = matcher(sent)
        # print(sent)
        # for token in sent:
        #   print(token.text, token.pos_, token.tag_)

        for match_id, start, end in matches:
            span = sent[start:end]
            phrase = span.text
            # if len(phrase.split()) > 2 and phrase.split()[1] == 'not':
            #   phrase = " ".join(phrase.split())
            # print(phrase)

        if len(phrase) > 0:
            return phrase
        else:
            return False
# 28

    def past_continuous(self, sent):
        phrase = ''
        matcher = Matcher(nlp.vocab)

        pattern_1 = [{'TAG': 'NNP'}, {"TEXT": "was"}, {'TAG': 'VBG'}]
        pattern_2 = [{'TAG': 'NNPS'}, {"TEXT": "was"}, {'TAG': 'VBG'}]
        pattern_3 = [{'TAG': 'NN'}, {"TEXT": "was"}, {'TAG': 'VBG'}]
        pattern_4 = [{'TAG': 'PRP'}, {"TEXT": "was"}, {'TAG': 'VBG'}]

        pattern_5 = [{'TAG': 'NNP'}, {"TEXT": "were"}, {'TAG': 'VBG'}]
        pattern_6 = [{'TAG': 'NNPS'}, {"TEXT": "were"}, {'TAG': 'VBG'}]
        pattern_7 = [{'TAG': 'NN'}, {"TEXT": "were"}, {'TAG': 'VBG'}]
        pattern_8 = [{'TAG': 'PRP'}, {"TEXT": "were"}, {'TAG': 'VBG'}]

        pattern_9 = [{"TEXT": "was"}, {'TAG': 'NNP'}, {'TAG': 'VBG'}]
        pattern_10 = [{"TEXT": "was"}, {'TAG': 'NNPS'}, {'TAG': 'VBG'}]
        pattern_11 = [{"TEXT": "was"}, {'TAG': 'NN'}, {'TAG': 'VBG'}]
        pattern_12 = [{"TEXT": "was"}, {'TAG': 'PRP'}, {'TAG': 'VBG'}]

        pattern_13 = [{"TEXT": "were"}, {'TAG': 'NNP'}, {'TAG': 'VBG'}]
        pattern_14 = [{"TEXT": "were"}, {'TAG': 'NNPS'}, {'TAG': 'VBG'}]
        pattern_15 = [{"TEXT": "were"}, {'TAG': 'NN'}, {'TAG': 'VBG'}]
        pattern_16 = [{"TEXT": "were"}, {'TAG': 'PRP'}, {'TAG': 'VBG'}]

        pattern_17 = [{'TAG': 'NNP'}, {"TEXT": "was"},
                      {"TAG": "RB"}, {'TAG': 'VBG'}]
        pattern_18 = [{'TAG': 'NNPS'}, {"TEXT": "was"},
                      {"TAG": "RB"}, {'TAG': 'VBG'}]
        pattern_19 = [{'TAG': 'NN'}, {"TEXT": "was"},
                      {"TAG": "RB"}, {'TAG': 'VBG'}]
        pattern_20 = [{'TAG': 'PRP'}, {"TEXT": "was"},
                      {"TAG": "RB"}, {'TAG': 'VBG'}]

        pattern_21 = [{'TAG': 'NNP'}, {"TEXT": "were"},
                      {"TAG": "RB"}, {'TAG': 'VBG'}]
        pattern_22 = [{'TAG': 'NNPS'}, {"TEXT": "were"},
                      {"TAG": "RB"}, {'TAG': 'VBG'}]
        pattern_23 = [{'TAG': 'NN'}, {"TEXT": "were"},
                      {"TAG": "RB"}, {'TAG': 'VBG'}]
        pattern_24 = [{'TAG': 'PRP'}, {"TEXT": "were"},
                      {"TAG": "RB"}, {'TAG': 'VBG'}]

        matcher.add('past_continuous', None,
                    pattern_1, pattern_2, pattern_3, pattern_4,
                    pattern_5, pattern_6, pattern_7, pattern_8,
                    pattern_9, pattern_10, pattern_11, pattern_12,
                    pattern_13, pattern_14, pattern_15, pattern_16,
                    pattern_17, pattern_18, pattern_19, pattern_20,
                    pattern_21, pattern_22, pattern_23, pattern_24,

                    )

        sent = nlp(sent.lower())
        matches = matcher(sent)
        # print(sent)
        # for token in sent:
        #   print(token.text, token.pos_, token.tag_)

        for match_id, start, end in matches:
            span = sent[start:end]
            phrase = span.text
            # if len(phrase.split()) > 2 and phrase.split()[1] == 'not':
            #   phrase = " ".join(phrase.split())
            # print(phrase)

        if len(phrase) > 0:
            return phrase
        else:
            return False
# 29

    def present_perfect(self, sent):
        phrase = ''
        matcher = Matcher(nlp.vocab)

        pattern_1 = [{'TAG': 'NN'}, {"TEXT": "have"}, {'TAG': 'VBN'}]
        pattern_2 = [{'TAG': 'NNS'}, {"TEXT": "have"}, {'TAG': 'VBN'}]
        pattern_3 = [{'TAG': 'NNP'}, {"TEXT": "have"}, {'TAG': 'VBN'}]
        pattern_4 = [{'TAG': 'NNPS'}, {"TEXT": "have"}, {'TAG': 'VBN'}]
        pattern_5 = [{'TAG': 'PRP'}, {"TEXT": "have"}, {'TAG': 'VBN'}]

        pattern_6 = [{'TAG': 'NN'}, {"TEXT": "has"}, {'TAG': 'VBN'}]
        pattern_7 = [{'TAG': 'NNS'}, {"TEXT": "has"}, {'TAG': 'VBN'}]
        pattern_8 = [{'TAG': 'NNP'}, {"TEXT": "has"}, {'TAG': 'VBN'}]
        pattern_9 = [{'TAG': 'NNPS'}, {"TEXT": "has"}, {'TAG': 'VBN'}]
        pattern_10 = [{'TAG': 'PRP'}, {"TEXT": "has"}, {'TAG': 'VBN'}]

        pattern_11 = [{"TEXT": "'ve"}, {'TAG': 'VBN'}]
        pattern_12 = [{"TEXT": "'ve"}, {'TAG': 'VBN'}]
        pattern_13 = [{"TEXT": "'ve"}, {'TAG': 'VBN'}]
        pattern_14 = [{"TEXT": "'ve"}, {'TAG': 'VBN'}]
        pattern_15 = [{"TEXT": "'ve"}, {'TAG': 'VBN'}]

        pattern_16 = [{"TEXT": "'s"}, {'TAG': 'VBN'}]
        pattern_17 = [{"TEXT": "'s"}, {'TAG': 'VBN'}]
        pattern_18 = [{"TEXT": "'s"}, {'TAG': 'VBN'}]
        pattern_19 = [{"TEXT": "'s"}, {'TAG': 'VBN'}]
        pattern_20 = [{"TEXT": "'s"}, {'TAG': 'VBN'}]

        pattern_21 = [{"TEXT": "have"}, {'TAG': 'NN'}, {'TAG': 'VBN'}]
        pattern_22 = [{"TEXT": "have"}, {'TAG': 'NNS'}, {'TAG': 'VBN'}]
        pattern_23 = [{"TEXT": "have"}, {'TAG': 'NNP'}, {'TAG': 'VBN'}]
        pattern_24 = [{"TEXT": "have"}, {'TAG': 'NNPS'}, {'TAG': 'VBN'}]
        pattern_25 = [{"TEXT": "have"}, {'TAG': 'PRP'}, {'TAG': 'VBN'}]

        pattern_26 = [{"TEXT": "has"}, {'TAG': 'NN'}, {'TAG': 'VBN'}]
        pattern_27 = [{"TEXT": "has"}, {'TAG': 'NNS'}, {'TAG': 'VBN'}]
        pattern_28 = [{"TEXT": "has"}, {'TAG': 'NNP'}, {'TAG': 'VBN'}]
        pattern_29 = [{"TEXT": "has"}, {'TAG': 'NNPS'}, {'TAG': 'VBN'}]
        pattern_30 = [{"TEXT": "has"}, {'TAG': 'PRP'}, {'TAG': 'VBN'}]

        matcher.add('past_continuous', None,
                    pattern_1, pattern_2, pattern_3, pattern_4, pattern_5,
                    pattern_6, pattern_7, pattern_8, pattern_9, pattern_10,
                    pattern_11, pattern_12, pattern_13, pattern_14, pattern_15,
                    pattern_16, pattern_17, pattern_18, pattern_19, pattern_20,
                    pattern_21, pattern_22, pattern_23, pattern_24, pattern_25,
                    pattern_26, pattern_27, pattern_28, pattern_29, pattern_30,

                    )

        sent = nlp(sent.lower())
        matches = matcher(sent)
        # print(sent)
        # for token in sent:
        #   print(token.text, token.pos_, token.tag_)

        for match_id, start, end in matches:
            span = sent[start:end]
            phrase = span.text
            # print(phrase)

        if len(phrase) > 0:
            return phrase
        else:
            return False
# 30

    def future_continuous(self, sent):
        phrase = ''
        matcher = Matcher(nlp.vocab)

        pattern_1 = [{'TAG': 'NN'}, {"TEXT": "will"},
                     {'TEXT': 'be'}, {'TAG': 'VBG'}]
        pattern_2 = [{'TAG': 'NNS'}, {"TEXT": "will"},
                     {'TEXT': 'be'}, {'TAG': 'VBG'}]
        pattern_3 = [{'TAG': 'NNP'}, {"TEXT": "will"},
                     {'TEXT': 'be'}, {'TAG': 'VBG'}]
        pattern_4 = [{'TAG': 'NNPS'}, {"TEXT": "will"},
                     {'TEXT': 'be'}, {'TAG': 'VBG'}]
        pattern_5 = [{'POS': 'PRON'}, {'TEXT': 'will'},
                     {'TEXT': 'be'}, {'TAG': 'VBG'}]

        pattern_6 = [{"TEXT": "'ll"}, {'TEXT': 'be'}, {'TAG': 'VBG'}]
        pattern_7 = [{"TEXT": "'ll"}, {'TEXT': 'be'}, {'TAG': 'VBG'}]
        pattern_8 = [{"TEXT": "'ll"}, {'TEXT': 'be'}, {'TAG': 'VBG'}]
        pattern_9 = [{"TEXT": "'ll"}, {'TEXT': 'be'}, {'TAG': 'VBG'}]
        pattern_10 = [{"TEXT": "'ll"}, {'TEXT': 'be'}, {'TAG': 'VBG'}]

        pattern_11 = [{"TEXT": "will"}, {'TAG': 'NN'},
                      {'TEXT': 'be'}, {'TAG': 'VBG'}]
        pattern_12 = [{"TEXT": "will"}, {'TAG': 'NNS'},
                      {'TEXT': 'be'}, {'TAG': 'VBG'}]
        pattern_13 = [{"TEXT": "will"}, {'TAG': 'NNP'},
                      {'TEXT': 'be'}, {'TAG': 'VBG'}]
        pattern_14 = [{"TEXT": "will"}, {'TAG': 'NNPS'},
                      {'TEXT': 'be'}, {'TAG': 'VBG'}]
        pattern_15 = [{"TEXT": "will"}, {'POS': 'PRON'},
                      {'TEXT': 'be'}, {'TAG': 'VBG'}]

        pattern_16 = [{'TAG': 'NN'}, {"TEXT": "will"}, {
            'TEXT': 'not'}, {'TEXT': 'be'}, {'TAG': 'VBG'}]
        pattern_17 = [{'TAG': 'NNS'}, {"TEXT": "will"}, {
            'TEXT': 'not'}, {'TEXT': 'be'}, {'TAG': 'VBG'}]
        pattern_18 = [{'TAG': 'NNP'}, {"TEXT": "will"}, {
            'TEXT': 'not'}, {'TEXT': 'be'}, {'TAG': 'VBG'}]
        pattern_19 = [{'TAG': 'NNPS'}, {"TEXT": "will"}, {
            'TEXT': 'not'}, {'TEXT': 'be'}, {'TAG': 'VBG'}]
        pattern_20 = [{'POS': 'PRON'}, {'TEXT': 'will'}, {
            'TEXT': 'not'}, {'TEXT': 'be'}, {'TAG': 'VBG'}]

        matcher.add('future_continuous', None,
                    pattern_1, pattern_2, pattern_3, pattern_4, pattern_5,
                    pattern_6, pattern_7, pattern_8, pattern_9, pattern_10,
                    pattern_11, pattern_12, pattern_13, pattern_14, pattern_15,
                    pattern_16, pattern_17, pattern_18, pattern_19, pattern_20, )

        sent = nlp(sent.lower())
        matches = matcher(sent)
        # print(sent)
        # for token in sent:
        #   print(token.text, token.pos_, token.tag_)

        for match_id, start, end in matches:
            span = sent[start:end]
            phrase = span.text
            # if len(phrase.split()) > 2 and phrase.split()[1] == 'not':
            #   phrase = " ".join(phrase.split())
            # print(phrase)

        if len(phrase) > 0:
            return phrase
        else:
            return False
# 31

    def questions(self, sent):
        has_questions = False
        sent = sent.lower()
        if sent[-1] == '?':
            matcher = Matcher(nlp.vocab)

            pattern_1 = [{'TAG': 'WP'}]
            pattern_2 = [{'TAG': 'WRB'}]
            pattern_3 = [{'TAG': 'PRP'}, {"TEXT": "?"}]

            if 'or' in sent and sent[-1] == '?':
                has_questions = True

            matcher.add('questions', None,
                        pattern_1, pattern_2, pattern_3

                        )

            sent = nlp(sent.lower())
            matches = matcher(sent)
            # print(sent)
            # for token in sent:
            #   print(token.text, token.pos_, token.tag_)

            for match_id, start, end in matches:
                span = sent[start:end]
                phrase = span.text

                has_questions = True
                # print(phrase)
                break
                # if len(phrase.split()) > 2 and phrase.split()[1] == 'not':
                #   phrase = " ".join(phrase.split())

        return has_questions
# 32

    def gerunds(self, sent):
        has_gerunds = False

        sent = sent.lower()

        matcher = Matcher(nlp.vocab)

        pattern_1 = [{'TAG': 'VBG'}, {"POS": "VERB"}]
        pattern_2 = [{"TAG": "IN"}, {'TAG': 'VBG'}, ]
        pattern_3 = [{'TAG': 'VBZ'}, {"TAG": "NN"}]
        pattern_4 = [{'TAG': 'VBG'}, {"TAG": "VBZ"}]

        if nlp(sent)[0].tag_ == "VBG":
            has_gerunds = True

        matcher.add('gerunds', None,
                    pattern_1,
                    pattern_2,
                    pattern_3,
                    pattern_4
                    )

        sent = nlp(sent)
        matches = matcher(sent)
        # print(sent)
        # for token in sent:
        #   print(token.text, token.pos_, token.tag_)

        for match_id, start, end in matches:
            span = sent[start:end]
            phrase = span.text
            has_gerunds = True
            # print(phrase)
            break

        return has_gerunds
# 33

    def connecting_words(self, sent):
        has_connecting_words = False
        connecting_words_list = ['because', 'since', 'as',
                                 'and so', 'because of', 'consequently', 'therefore', ]

        sent = [str(token).lower() for token in nlp(sent)]
        for word in sent:
            if word in connecting_words_list:
                has_connecting_words = True
                break

        return has_connecting_words
# 34

    def past_perfect(self, sent):
        phrase = ''
        matcher = Matcher(nlp.vocab)

        pattern_1 = [{'TAG': 'NN'}, {"TEXT": "had"}, {'TAG': 'VBN'}]
        pattern_2 = [{'TAG': 'NNS'}, {"TEXT": "had"}, {'TAG': 'VBN'}]
        pattern_3 = [{'TAG': 'NNP'}, {"TEXT": "had"}, {'TAG': 'VBN'}]
        pattern_4 = [{'TAG': 'NNPS'}, {"TEXT": "had"}, {'TAG': 'VBN'}]
        pattern_5 = [{'TAG': 'PRP'}, {"TEXT": "had"}, {'TAG': 'VBN'}]

        pattern_6 = [{"TEXT": "'d"}, {'TAG': 'VBN'}]
        pattern_7 = [{"TEXT": "'d"}, {'TAG': 'VBN'}]
        pattern_8 = [{"TEXT": "'d"}, {'TAG': 'VBN'}]
        pattern_9 = [{"TEXT": "'d"}, {'TAG': 'VBN'}]
        pattern_10 = [{"TEXT": "'d"}, {'TAG': 'VBN'}]

        pattern_11 = [{"TEXT": "had"}, {'TAG': 'NN'}, {'TAG': 'VBN'}]
        pattern_12 = [{"TEXT": "had"}, {'TAG': 'NNS'}, {'TAG': 'VBN'}]
        pattern_13 = [{"TEXT": "had"}, {'TAG': 'NNP'}, {'TAG': 'VBN'}]
        pattern_14 = [{"TEXT": "had"}, {'TAG': 'NNPS'}, {'TAG': 'VBN'}]
        pattern_15 = [{"TEXT": "had"}, {'TAG': 'PRP'}, {'TAG': 'VBN'}]

        pattern_16 = [{'TAG': 'NN'}, {"TEXT": "had"},
                      {"TAG": "RB"}, {'TAG': 'VBN'}]
        pattern_17 = [{'TAG': 'NNS'}, {"TEXT": "had"},
                      {"TAG": "RB"}, {'TAG': 'VBN'}]
        pattern_18 = [{'TAG': 'NNP'}, {"TEXT": "had"},
                      {"TAG": "RB"}, {'TAG': 'VBN'}]
        pattern_19 = [{'TAG': 'NNPS'}, {"TEXT": "had"},
                      {"TAG": "RB"}, {'TAG': 'VBN'}]
        pattern_20 = [{'TAG': 'PRP'}, {"TEXT": "had"},
                      {"TAG": "RB"}, {'TAG': 'VBN'}]

        pattern_21 = [{"TEXT": "'d"}, {"TAG": "RB"}, {'TAG': 'VBN'}]
        pattern_22 = [{"TEXT": "'d"}, {"TAG": "RB"}, {'TAG': 'VBN'}]
        pattern_23 = [{"TEXT": "'d"}, {"TAG": "RB"}, {'TAG': 'VBN'}]
        pattern_24 = [{"TEXT": "'d"}, {"TAG": "RB"}, {'TAG': 'VBN'}]
        pattern_25 = [{"TEXT": "'d"}, {"TAG": "RB"}, {'TAG': 'VBN'}]

        pattern_26 = [{"TEXT": "had"}, {'TAG': 'NN'},
                      {"TAG": "RB"}, {'TAG': 'VBN'}]
        pattern_27 = [{"TEXT": "had"}, {'TAG': 'NNS'},
                      {"TAG": "RB"}, {'TAG': 'VBN'}]
        pattern_28 = [{"TEXT": "had"}, {'TAG': 'NNP'},
                      {"TAG": "RB"}, {'TAG': 'VBN'}]
        pattern_29 = [{"TEXT": "had"}, {'TAG': 'NNPS'},
                      {"TAG": "RB"}, {'TAG': 'VBN'}]
        pattern_30 = [{"TEXT": "had"}, {'TAG': 'PRP'},
                      {"TAG": "RB"}, {'TAG': 'VBN'}]

        matcher.add('past_perfect', None,
                    pattern_1, pattern_2, pattern_3, pattern_4, pattern_5,
                    pattern_6, pattern_7, pattern_8, pattern_9, pattern_10,
                    pattern_11, pattern_12, pattern_13, pattern_14, pattern_15,
                    pattern_16, pattern_17, pattern_18, pattern_19, pattern_20,
                    pattern_21, pattern_22, pattern_23, pattern_24, pattern_25,
                    pattern_26, pattern_27, pattern_28, pattern_29, pattern_30,

                    )

        sent = nlp(sent.lower())
        matches = matcher(sent)
        # print(sent)
        # for token in sent:
        #   print(token.text, token.pos_, token.tag_)

        for match_id, start, end in matches:
            span = sent[start:end]
            phrase = span.text
            # print(phrase)

        if len(phrase) > 0:
            return phrase
        else:
            return False
# 35

    def present_perfect_continuous(self, sent):
        phrase = ''
        matcher = Matcher(nlp.vocab)

        pattern_1 = [{'TAG': 'NN'}, {"TEXT": "have"},
                     {"TEXT": "been"}, {'TAG': 'VBG'}]
        pattern_2 = [{'TAG': 'NNS'}, {"TEXT": "have"},
                     {"TEXT": "been"}, {'TAG': 'VBG'}]
        pattern_3 = [{'TAG': 'NNP'}, {"TEXT": "have"},
                     {"TEXT": "been"}, {'TAG': 'VBG'}]
        pattern_4 = [{'TAG': 'NNPS'}, {"TEXT": "have"},
                     {"TEXT": "been"}, {'TAG': 'VBG'}]
        pattern_5 = [{'TAG': 'PRP'}, {"TEXT": "have"},
                     {"TEXT": "been"}, {'TAG': 'VBG'}]

        pattern_6 = [{'TAG': 'NN'}, {"TEXT": "has"},
                     {"TEXT": "been"}, {'TAG': 'VBG'}]
        pattern_7 = [{'TAG': 'NNS'}, {"TEXT": "has"},
                     {"TEXT": "been"}, {'TAG': 'VBG'}]
        pattern_8 = [{'TAG': 'NNP'}, {"TEXT": "has"},
                     {"TEXT": "been"}, {'TAG': 'VBG'}]
        pattern_9 = [{'TAG': 'NNPS'}, {"TEXT": "has"},
                     {"TEXT": "been"}, {'TAG': 'VBG'}]
        pattern_10 = [{'TAG': 'PRP'}, {"TEXT": "has"},
                      {"TEXT": "been"}, {'TAG': 'VBG'}]

        pattern_11 = [{"TEXT": "'ve"}, {"TEXT": "been"}, {'TAG': 'VBG'}]
        pattern_12 = [{"TEXT": "'ve"}, {"TEXT": "been"}, {'TAG': 'VBG'}]
        pattern_13 = [{"TEXT": "'ve"}, {"TEXT": "been"}, {'TAG': 'VBG'}]
        pattern_14 = [{"TEXT": "'ve"}, {"TEXT": "been"}, {'TAG': 'VBG'}]
        pattern_15 = [{"TEXT": "'ve"}, {"TEXT": "been"}, {'TAG': 'VBG'}]

        pattern_16 = [{"TEXT": "'s"}, {"TEXT": "been"}, {'TAG': 'VBG'}]
        pattern_17 = [{"TEXT": "'s"}, {"TEXT": "been"}, {'TAG': 'VBG'}]
        pattern_18 = [{"TEXT": "'s"}, {"TEXT": "been"}, {'TAG': 'VBG'}]
        pattern_19 = [{"TEXT": "'s"}, {"TEXT": "been"}, {'TAG': 'VBG'}]
        pattern_20 = [{"TEXT": "'s"}, {"TEXT": "been"}, {'TAG': 'VBG'}]

        pattern_21 = [{"TEXT": "have"}, {'TAG': 'NN'},
                      {"TEXT": "been"}, {'TAG': 'VBG'}]
        pattern_22 = [{"TEXT": "have"}, {'TAG': 'NNS'},
                      {"TEXT": "been"}, {'TAG': 'VBG'}]
        pattern_23 = [{"TEXT": "have"}, {'TAG': 'NNP'},
                      {"TEXT": "been"}, {'TAG': 'VBG'}]
        pattern_24 = [{"TEXT": "have"}, {'TAG': 'NNPS'},
                      {"TEXT": "been"}, {'TAG': 'VBG'}]
        pattern_25 = [{"TEXT": "have"}, {'TAG': 'PRP'},
                      {"TEXT": "been"}, {'TAG': 'VBG'}]

        pattern_26 = [{"TEXT": "has"}, {'TAG': 'NN'},
                      {"TEXT": "been"}, {'TAG': 'VBG'}]
        pattern_27 = [{"TEXT": "has"}, {'TAG': 'NNS'},
                      {"TEXT": "been"}, {'TAG': 'VBG'}]
        pattern_28 = [{"TEXT": "has"}, {'TAG': 'NNP'},
                      {"TEXT": "been"}, {'TAG': 'VBG'}]
        pattern_29 = [{"TEXT": "has"}, {'TAG': 'NNPS'},
                      {"TEXT": "been"}, {'TAG': 'VBG'}]
        pattern_30 = [{"TEXT": "has"}, {'TAG': 'PRP'},
                      {"TEXT": "been"}, {'TAG': 'VBG'}]

        matcher.add('present_perfect_continuous', None,
                    pattern_1, pattern_2, pattern_3, pattern_4, pattern_5,
                    pattern_6, pattern_7, pattern_8, pattern_9, pattern_10,
                    pattern_11, pattern_12, pattern_13, pattern_14, pattern_15,
                    pattern_16, pattern_17, pattern_18, pattern_19, pattern_20,
                    pattern_21, pattern_22, pattern_23, pattern_24, pattern_25,
                    pattern_26, pattern_27, pattern_28, pattern_29, pattern_30,
                    )

        sent = nlp(sent.lower())
        matches = matcher(sent)
        # print(sent)
        # for token in sent:
        #   print(token.text, token.pos_, token.tag_)

        for match_id, start, end in matches:
            span = sent[start:end]
            phrase = span.text
            # print(phrase)

        if len(phrase) > 0:
            return phrase
        else:
            return False
# 36

    def future_perfect_continuous(self, sent):
        phrase = ''
        matcher = Matcher(nlp.vocab)

        pattern_1 = [{'TAG': 'NN'}, {"TEXT": "will"}, {
            "TEXT": "have"}, {"TEXT": "been"}, {'TAG': 'VBG'}]
        pattern_2 = [{'TAG': 'NNS'}, {"TEXT": "will"}, {
            "TEXT": "have"}, {"TEXT": "been"}, {'TAG': 'VBG'}]
        pattern_3 = [{'TAG': 'NNP'}, {"TEXT": "will"}, {
            "TEXT": "have"}, {"TEXT": "been"}, {'TAG': 'VBG'}]
        pattern_4 = [{'TAG': 'NNPS'}, {"TEXT": "will"}, {
            "TEXT": "have"}, {"TEXT": "been"}, {'TAG': 'VBG'}]
        pattern_5 = [{'TAG': 'PRP'}, {"TEXT": "will"}, {
            "TEXT": "have"}, {"TEXT": "been"}, {'TAG': 'VBG'}]

        pattern_6 = [{"TEXT": "will"}, {'TAG': 'NN'}, {
            "TEXT": "have"}, {"TEXT": "been"}, {'TAG': 'VBG'}]
        pattern_7 = [{"TEXT": "will"}, {'TAG': 'NNS'}, {
            "TEXT": "have"}, {"TEXT": "been"}, {'TAG': 'VBG'}]
        pattern_8 = [{"TEXT": "will"}, {'TAG': 'NNP'}, {
            "TEXT": "have"}, {"TEXT": "been"}, {'TAG': 'VBG'}]
        pattern_9 = [{"TEXT": "will"}, {'TAG': 'NNPS'}, {
            "TEXT": "have"}, {"TEXT": "been"}, {'TAG': 'VBG'}]
        pattern_10 = [{"TEXT": "will"}, {'TAG': 'PRP'}, {
            "TEXT": "have"}, {"TEXT": "been"}, {'TAG': 'VBG'}]

        matcher.add('future_perfect_continuous', None,
                    pattern_1, pattern_2, pattern_3, pattern_4, pattern_5,
                    pattern_6, pattern_7, pattern_8, pattern_9, pattern_10,

                    )

        sent = nlp(sent.lower())
        matches = matcher(sent)
        # print(sent)
        # for token in sent:
        #   print(token.text, token.pos_, token.tag_)

        for match_id, start, end in matches:
            span = sent[start:end]
            phrase = span.text
            # print(phrase)

        if len(phrase) > 0:
            return phrase
        else:
            return False
# 37

    def past_perfect_continuous(self, sent):
        phrase = ''
        matcher = Matcher(nlp.vocab)

        pattern_1 = [{'TAG': 'NN'}, {"TEXT": "had"},
                     {"TEXT": "been"}, {'TAG': 'VBG'}]
        pattern_2 = [{'TAG': 'NNS'}, {"TEXT": "had"},
                     {"TEXT": "been"}, {'TAG': 'VBG'}]
        pattern_3 = [{'TAG': 'NNP'}, {"TEXT": "had"},
                     {"TEXT": "been"}, {'TAG': 'VBG'}]
        pattern_4 = [{'TAG': 'NNPS'}, {"TEXT": "had"},
                     {"TEXT": "been"}, {'TAG': 'VBG'}]
        pattern_5 = [{'TAG': 'PRP'}, {"TEXT": "had"},
                     {"TEXT": "been"}, {'TAG': 'VBG'}]

        pattern_6 = [{"TEXT": "had"}, {'TAG': 'NN'},
                     {"TEXT": "been"}, {'TAG': 'VBG'}]
        pattern_7 = [{"TEXT": "had"}, {'TAG': 'NNS'},
                     {"TEXT": "been"}, {'TAG': 'VBG'}]
        pattern_8 = [{"TEXT": "had"}, {'TAG': 'NNP'},
                     {"TEXT": "been"}, {'TAG': 'VBG'}]
        pattern_9 = [{"TEXT": "had"}, {'TAG': 'NNPS'},
                     {"TEXT": "been"}, {'TAG': 'VBG'}]
        pattern_10 = [{"TEXT": "had"}, {'TAG': 'PRP'},
                      {"TEXT": "been"}, {'TAG': 'VBG'}]

        matcher.add('past_perfect_continuous', None,
                    pattern_1, pattern_2, pattern_3, pattern_4, pattern_5,
                    pattern_6, pattern_7, pattern_8, pattern_9, pattern_10,

                    )

        sent = nlp(sent.lower())
        matches = matcher(sent)
        # print(sent)
        # for token in sent:
        #   print(token.text, token.pos_, token.tag_)

        for match_id, start, end in matches:
            span = sent[start:end]
            phrase = span.text
            # print(phrase)

        if len(phrase) > 0:
            return phrase
        else:
            return False
# 38

    def future_perfect(self, sent):
        phrase = ''
        matcher = Matcher(nlp.vocab)

        pattern_1 = [{'TAG': 'NN'}, {"TEXT": "will"},
                     {"TEXT": "have"}, {'TAG': 'VBN'}]
        pattern_2 = [{'TAG': 'NNS'}, {"TEXT": "will"},
                     {"TEXT": "have"}, {'TAG': 'VBN'}]
        pattern_3 = [{'TAG': 'NNP'}, {"TEXT": "will"},
                     {"TEXT": "have"}, {'TAG': 'VBN'}]
        pattern_4 = [{'TAG': 'NNPS'}, {"TEXT": "will"},
                     {"TEXT": "have"}, {'TAG': 'VBN'}]
        pattern_5 = [{'TAG': 'PRP'}, {"TEXT": "will"},
                     {"TEXT": "have"}, {'TAG': 'VBN'}]

        pattern_6 = [{"TEXT": "will"}, {'TAG': 'NN'},
                     {"TEXT": "have"}, {'TAG': 'VBN'}]
        pattern_7 = [{"TEXT": "will"}, {'TAG': 'NNS'},
                     {"TEXT": "have"}, {'TAG': 'VBN'}]
        pattern_8 = [{"TEXT": "will"}, {'TAG': 'NNP'},
                     {"TEXT": "have"}, {'TAG': 'VBN'}]
        pattern_9 = [{"TEXT": "will"}, {'TAG': 'NNPS'},
                     {"TEXT": "have"}, {'TAG': 'VBN'}]
        pattern_10 = [{"TEXT": "will"}, {'TAG': 'PRP'},
                      {"TEXT": "have"}, {'TAG': 'VBN'}]

        pattern_11 = [{"TEXT": "have"}, {'TAG': 'NN'},
                      {"TEXT": "been"}, {'TAG': 'VBG'}]
        pattern_12 = [{"TEXT": "have"}, {'TAG': 'NNS'},
                      {"TEXT": "been"}, {'TAG': 'VBG'}]
        pattern_13 = [{"TEXT": "have"}, {'TAG': 'NNP'},
                      {"TEXT": "been"}, {'TAG': 'VBG'}]
        pattern_14 = [{"TEXT": "have"}, {'TAG': 'NNPS'},
                      {"TEXT": "been"}, {'TAG': 'VBG'}]
        pattern_15 = [{"TEXT": "have"}, {'TAG': 'PRP'},
                      {"TEXT": "been"}, {'TAG': 'VBG'}]

        matcher.add('future_perfect', None,
                    pattern_1, pattern_2, pattern_3, pattern_4, pattern_5,
                    pattern_6, pattern_7, pattern_8, pattern_9, pattern_10,
                    pattern_11, pattern_12, pattern_13, pattern_14, pattern_15,

                    )

        sent = nlp(sent.lower())
        matches = matcher(sent)
        # print(sent)
        # for token in sent:
        #   print(token.text, token.pos_, token.tag_)

        for match_id, start, end in matches:
            span = sent[start:end]
            phrase = span.text
            # print(phrase)

        if len(phrase) > 0:
            return phrase
        else:
            return False
# 39

    def simple_passive(self, sent):
        phrase = ''
        matcher = Matcher(nlp.vocab)

        pattern_1 = [{'TAG': 'NNP'}, {"TEXT": "am"}, {'TAG': 'VBN'}]
        pattern_2 = [{'TAG': 'NNPS'}, {"TEXT": "am"}, {'TAG': 'VBN'}]
        pattern_3 = [{'TAG': 'NN'}, {"TEXT": "am"}, {'TAG': 'VBN'}]
        pattern_4 = [{'TAG': 'PRP'}, {"TEXT": "am"}, {'TAG': 'VBN'}]

        pattern_5 = [{'TAG': 'NNP'}, {"TEXT": "is"}, {'TAG': 'VBN'}]
        pattern_6 = [{'TAG': 'NNPS'}, {"TEXT": "is"}, {'TAG': 'VBN'}]
        pattern_7 = [{'TAG': 'NN'}, {"TEXT": "is"}, {'TAG': 'VBN'}]
        pattern_8 = [{'TAG': 'PRP'}, {"TEXT": "is"}, {'TAG': 'VBN'}]

        pattern_9 = [{'TAG': 'NNP'}, {"TEXT": "are"}, {'TAG': 'VBN'}]
        pattern_10 = [{'TAG': 'NNPS'}, {"TEXT": "are"}, {'TAG': 'VBN'}]
        pattern_11 = [{'TAG': 'NNS'}, {"TEXT": "are"}, {'TAG': 'VBN'}]
        pattern_12 = [{'TAG': 'PRP'}, {"TEXT": "are"}, {'TAG': 'VBN'}]

        pattern_13 = [{"TEXT": "am"}, {'TAG': 'NNP'}, {'TAG': 'VBN'}]
        pattern_14 = [{"TEXT": "am"}, {'TAG': 'NNPS'}, {'TAG': 'VBN'}]
        pattern_15 = [{"TEXT": "am"}, {'TAG': 'NN'}, {'TAG': 'VBN'}]
        pattern_16 = [{"TEXT": "am"}, {'TAG': 'PRP'}, {'TAG': 'VBN'}]

        pattern_17 = [{"TEXT": "is"}, {'TAG': 'NNP'}, {'TAG': 'VBN'}]
        pattern_18 = [{"TEXT": "is"}, {'TAG': 'NNPS'}, {'TAG': 'VBN'}]
        pattern_19 = [{"TEXT": "is"}, {'TAG': 'NN'}, {'TAG': 'VBN'}]
        pattern_20 = [{"TEXT": "is"}, {'TAG': 'PRP'}, {'TAG': 'VBG'}]

        pattern_21 = [{"TEXT": "are"}, {'TAG': 'NNP'}, {'TAG': 'VBN'}]
        pattern_22 = [{"TEXT": "are"}, {'TAG': 'NNPS'}, {'TAG': 'VBN'}]
        pattern_23 = [{"TEXT": "are"}, {'TAG': 'NNS'}, {'TAG': 'VBN'}]
        pattern_24 = [{"TEXT": "are"}, {'TAG': 'PRP'}, {'TAG': 'VBN'}]

        pattern_25 = [{'TAG': 'NNP'}, {"TAG": "VBP"},
                      {"TEXT": "not"}, {'TAG': 'VBN'}]
        pattern_26 = [{'TAG': 'NNPS'}, {"TAG": "VBP"},
                      {"TEXT": "not"}, {'TAG': 'VBN'}]
        pattern_27 = [{'TAG': 'NN'}, {"TAG": "VBP"},
                      {"TEXT": "not"}, {'TAG': 'VBN'}]
        pattern_28 = [{'POS': 'PRON'}, {"TAG": "VBP"},
                      {"TEXT": "not"}, {'TAG': 'VBN'}]

        pattern_29 = [{'TAG': 'NNP'}, {"TAG": "VBZ"},
                      {"TEXT": "not"}, {'TAG': 'VBN'}]
        pattern_30 = [{'TAG': 'NNPS'}, {"TAG": "VBZ"},
                      {"TEXT": "not"}, {'TAG': 'VBN'}]
        pattern_31 = [{'TAG': 'NN'}, {"TAG": "VBZ"},
                      {"TEXT": "not"}, {'TAG': 'VBN'}]
        pattern_32 = [{'TAG': 'PRP'}, {"TAG": "VBZ"},
                      {"TEXT": "not"}, {'TAG': 'VBN'}]

        pattern_33 = [{'TAG': 'NNP'}, {"TEXT": "are not"}, {'TAG': 'VBN'}]
        pattern_34 = [{'TAG': 'NNPS'}, {"TEXT": "are not"}, {'TAG': 'VBN'}]
        pattern_35 = [{'TAG': 'NNS'}, {"TEXT": "are not"}, {'TAG': 'VBN'}]
        pattern_36 = [{'TAG': 'PRP'}, {"TEXT": "are not"}, {'TAG': 'VBN'}]

        matcher.add('simple_passive', None,
                    pattern_1, pattern_2, pattern_3, pattern_4,
                    pattern_5, pattern_6, pattern_7, pattern_8,
                    pattern_9, pattern_10, pattern_11, pattern_12,
                    pattern_13, pattern_14, pattern_15, pattern_16,
                    pattern_17, pattern_18, pattern_19, pattern_20,
                    pattern_21, pattern_22, pattern_23, pattern_24,
                    pattern_25, pattern_26, pattern_27, pattern_28,
                    pattern_29, pattern_30, pattern_31, pattern_32,
                    pattern_33, pattern_34, pattern_35, pattern_36,)

        sent = nlp(sent.lower())
        matches = matcher(sent)
        # print(sent)
        # for token in sent:
        #   print(token.text, token.pos_, token.tag_)

        for match_id, start, end in matches:
            span = sent[start:end]
            phrase = span.text
            # if len(phrase.split()) > 2 and phrase.split()[1] == 'not':
            #   phrase = " ".join(phrase.split())
            # print(phrase)

        if len(phrase) > 0:
            return phrase
        else:
            return False
# 40

    def perfect_modals(self, sent):
        phrase = ''
        matcher = Matcher(nlp.vocab, validate=True)

        # pattern_1 = [{"TEXT": "can't"},{"TEXT":"have"},{"TAG": "VBN"}]
        pattern_1 = [{"TEXT": "n't"}, {"TEXT": "have"}, {"TAG": "VBN"}]
        pattern_2 = [{"TEXT": "n’t"}, {"TEXT": "have"}, {"TAG": "VBN"}]

        matcher.add('perfect_modals', None,
                    pattern_1, pattern_2
                    )

        sent = nlp(sent.lower())
        matches = matcher(sent)
        # print(sent)
        # for token in sent:
        #   print(token.text, token.pos_, token.tag_)

        for match_id, start, end in matches:
            span = sent[start:end]
            phrase = span.text
            # if len(phrase.split()) > 2 and phrase.split()[1] == 'not':
            #   phrase = " ".join(phrase.split())
            # print(phrase)

        if len(phrase) > 0:
            return phrase
        else:
            return False
# 41

    def expressing_habits(self, sent):
        has_expressing_habits = False

        sent = sent.lower()
        # sent = [str(token).lower() for token in nlp(sent)]
        expressing_habits_list = ["used to", "would"]
        for word in expressing_habits_list:
            if word in sent:
                has_expressing_habits = True
                break

        if not has_expressing_habits:
            if self.past_simple(sent):
                has_expressing_habits = True

        return has_expressing_habits
