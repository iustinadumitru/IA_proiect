import re
import nltk
import heapq
import pprint
import traceback

from nltk.corpus import stopwords
from gensim.models import Word2Vec
from pattern3.text import singularize


# nltk.download('punkt')


def process_text(input_text, alpha):
    """
    Function that processes the input_text according to the alpha summarization percentage and returns the summarized text and no error message (None).
    In case of error, if returns an empty string ('') and a suggestive error message (eg: 'input text too long').
    :param input_text: the input text
    :param alpha: the summarization percentage
    :return: output_text, error (None if )
    """
    try:
        try:
            alpha = int(alpha)
        except Exception as e:
            alpha = 10
        if alpha < 10: alpha = 10
        if alpha > 50: alpha = 50

        text = input_text

        # Preprocessing the data
        text = re.sub(r'\[[0-9]*\]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        clean_text = text.lower()
        clean_text = re.sub(r'\W', ' ', clean_text)
        clean_text = re.sub(r'\d', ' ', clean_text)
        clean_text = re.sub(r'\s+', ' ', clean_text)

        # Tokenize sentences
        sentences = nltk.sent_tokenize(text)

        # Stopword list
        stop_words = nltk.corpus.stopwords.words('romanian')

        # Word counts
        word2count = {}
        for word in nltk.word_tokenize(clean_text):
            if word not in stop_words:
                if word not in word2count.keys():
                    word2count[word] = 1
                else:
                    word2count[word] += 1

        # Converting counts to weights
        max_count = max(word2count.values())
        for key in word2count.keys():
            word2count[key] = word2count[key] / max_count

        # Product sentence scores
        sent2score = {}
        for sentence in sentences:
            for word in nltk.word_tokenize(sentence.lower()):
                if word in word2count.keys():
                    if sentence not in sent2score.keys():
                        sent2score[sentence] = word2count[word]
                    else:
                        sent2score[sentence] += word2count[word]

        # Gettings best n lines
        sentences_number = int(len(sent2score) - ((alpha / 100) * len(sent2score)))

        sent2score = filter_sentences(sent2score)

        best_sentences = heapq.nlargest(sentences_number, sent2score, key=sent2score.get)

        # Order sentences in chronological order
        ordered_sentences = list()

        for prop in sent2score.keys():
            if prop in best_sentences:
                ordered_sentences.append(prop)

        output = ''
        for sentence in ordered_sentences:
            output += sentence + '\n\n'
        output = output[:-1]
        return output, None
    except Exception as e:
        print(traceback.format_exc())
        return '', 'error message'


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
             word2count: dictionary like: {"word": {"en": "word_in_en",
                                                    "count": 1(number)}}
             dictionary_text: matrix with word from one sentence
    """
    import googletrans

    word_trans = googletrans.Translator()

    stop_words = nltk.corpus.stopwords.words('romanian')
    word2count = {}
    dictionary_text = []
    count_sentence = 0
    for sentence in nltk.sent_tokenize(input_text):
        count_sentence += 1
        sentence_words = []
        for _word in nltk.word_tokenize(sentence):
            if _word not in stop_words:
                sentence_words.append(_word.lower())
                if _word not in word2count.keys():
                    word_in_en = word_trans.translate(_word, "en").text
                    word_in_en = singularize(word_in_en)
                    flag_en = 0
                    for en_word in word2count.values():
                        if en_word['en'] == word_in_en:
                            en_word['count'] += 1
                            flag_en = 1
                    if flag_en == 0:
                        word2count.update({_word: {"en": word_in_en, "count": 1}})
                else:
                    word2count[_word]["count"] += 1
        dictionary_text.append(sentence_words)

    print("Finish to process: {} sentences".format(count_sentence))
    return word2count, dictionary_text


def _startswith(sentence, prefix_list):
    for prefix in prefix_list:
        if sentence.startswith(prefix):
            return True
    return False


if __name__ == "__main__":
    input_text = ""
    # elupoae
    output = find_singularity(input_text)

    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(output[0])
    print(output[1])

    vocabulary = Word2Vec(output[1], min_count=1, size=100, window=5, sg=0)
    print(vocabulary.wv.vocab.keys())
