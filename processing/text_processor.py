import re
import nltk
import heapq
import urllib.request
import bs4 as bs
from googletrans import Translator

nltk.download('stopwords')


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

        # translator = Translator()
        # translated_input = translator.translate(input_text, src='ro').text
        # return translated_input, None

        # Gettings the data source
        # source = urllib.request.urlopen('http://www.istoria.md/articol/507/Mihai_Eminescu,_biografie').read()
        #
        # # Parsing the data/ creating BeautifulSoup object
        # soup = bs.BeautifulSoup(source, 'lxml')
        #
        # # Fetching the data
        # text = ""
        # for paragraph in soup.find_all('p'):
        #     text += paragraph.text
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
                    if len(sentence.split(' ')) < 25:
                        if sentence not in sent2score.keys():
                            sent2score[sentence] = word2count[word]
                        else:
                            sent2score[sentence] += word2count[word]

        # Gettings best n lines
        sentences_number = int(len(sent2score) - ((alpha / 100) * len(sent2score)))

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
        # return '', 'error message'
        import traceback
        return '', traceback.format_exc()
