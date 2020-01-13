from rippletagger.tagger import Tagger
from processing.text_processor import find_singularity
from collections import defaultdict

import nltk

word_to_english = dict()
#this dictionary will register the translation of a word
#word_to_english["caine"] = "dog"

WORD_COUNT = {}
PARAGRAPH_UPDATE_CONSTANT = 0.2
ALPHA = 10
ORIGINAL_TEXT = ""
_SCORES = defaultdict(lambda: 0)
scores_points = {
    "PROPN": 4,
    "NOUN": 2,
    "VERB": 2,
    "OTHER": 1
}

word_score = dict()
# this dictionary will register the score of a english word
# this 2 are used when updating / querry - ing a word
# update : word_score[word_to_english[word]] += new_score
# querry : word_score[word_to_english[word]]


def __getattr__(name):
    if name == "SCORES":
        if _SCORES == {}:
            """
            Acts as a property, will be used as "globals.SCORES[word]"
            
            Function that assigns a specific score to words based on their sentence parts
                proper noun = +4 score
                noun = +2 score
                verb = +2 score
                other = +1 score

            :param words: a dictionary for the words, where keys are the word in romanian and words[key] is the information
                about the respective word (output from 'find_singularity' function)

            :return: dictionary where each pair (key, value) will be (word, score_of_word)
            """

            stop_words = nltk.corpus.stopwords.words('english')
            word_count, text_sentences, vocabulary = find_singularity(ORIGINAL_TEXT)
            tagger = Tagger(language='ro')

            for sentence_as_list in text_sentences:
                sentence = tagger.tag(" ".join(sentence_as_list))
                for word in sentence:
                    word_in_en = word[0]
                    sentence_part = word[1]

                    if word_in_en in stop_words:
                        continue

                    if sentence_part in scores_points.keys():
                        _SCORES[word_in_en] += scores_points[sentence_part]

                    else:
                        _SCORES[word_in_en] += scores_points["OTHER"]

        return _SCORES


def get_hashed_english_word(word):
    if word.lower() in word_to_english.keys():
        return (word_to_english[word.lower()]).lower()
    return "WORD NOT FOUND IN DICT!!"


def get_word_score(word):
    english_word = get_hashed_english_word(word)
    if english_word == "WORD NOT FOUND IN DICT!!":
        return 0
    return word_score[english_word]


def add_word_to_english_dict(word_ro, word_en):
    if word_ro.lower() not in word_to_english:
        word_to_english[word_ro.lower()] = word_en
