import re
import nltk
from collections import defaultdict

from processing.translator import Translator
from gensim.models import Word2Vec
from nltk.stem.porter import PorterStemmer


# nltk.download('punkt')
def filter_sentences(sentences):
    res_sentences = dict()
    for sentence in sentences.keys():
        # dialogue
        if re.match(r'-\s*', sentence) or re.match(r'—\s*', sentence, re.UNICODE):
            continue
        # blacklist
        if _startswith(sentence,
                       ['A ', 'Au ', 'Asta a ', 'Aceasta a ', 'Acesta a ', 'Acestia au ', 'El ', 'Ea ', 'Ei ', 'Ele ']):
            continue
        res_sentences[sentence] = sentences[sentence]
    return res_sentences


def find_singularity(input_text):
    """
    :param input_text: original text
    :return: (word2count, dictionary_text)
             word2count: dictionary like: {"word_en": count(number)}
             dictionary_text: matrix with word from one sentence
             vocabulary: vocabulary of word from input_text, accomplished with Word2Vec
    """

    stemmer_singular = PorterStemmer()
    stop_words = nltk.corpus.stopwords.words('english')

    tr = Translator()
    words = tr.translate_words(nltk.word_tokenize(input_text))
    word2count = defaultdict(lambda: 0)
    output_count = defaultdict(lambda: 0)
    dictionary_text = []
    count_sentence = 0

    for sentence in nltk.sent_tokenize(input_text):
        sentence_en = []
        sentence = list(filter(lambda x: x not in ".,!?\"\'„”;", nltk.word_tokenize(sentence)))
        length = len(sentence)
        for word_ro, word_en in words[count_sentence: length + count_sentence]:
            if word_en not in stop_words:
                word_singular = stemmer_singular.stem(word_en)
                if word_singular + "e" == word_en:
                    word_singular = word_en

                word2count[word_singular] += 1
                sentence_en.append(word_singular)

            else:
                word2count[word_en] += 1
                sentence_en.append(word_en)

        dictionary_text.append(sentence_en)
        count_sentence += length

    for word_ro, word_en in words:
        if word_en not in stop_words:
            word_singular = stemmer_singular.stem(word_en)
            if word_singular + "e" == word_en:
                word_singular = word_en

            output_count[word_ro] = word2count[word_singular]

        else:
            output_count[word_ro] = word2count[word_en]

    vocabulary = Word2Vec(dictionary_text, min_count=1, size=100, window=5, sg=1)

    print("Finish to process: {} words".format(count_sentence))
    return output_count, dictionary_text, vocabulary

def _startswith(sentence, prefix_list):
    for prefix in prefix_list:
        if sentence.startswith(prefix):
            return True
    return False


if __name__ == "__main__":
    input_text = """"""

    output = find_singularity(input_text)
    vocabulary = output[2]
    print(output[0])
    # print(vocabulary)
