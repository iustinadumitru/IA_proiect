import re
import nltk
import heapq
import traceback

from processing import globals
from collections import defaultdict
from processing.globals import get_word_score, PARAGRAPH_UPDATE_CONSTANT
from processing.remove_dialog_v2 import remove_dialog
#from processing.text_name_processor import get_principal_character_name, set_max_score_sentence_with_best_name
from processing.text_processor import filter_sentences
from processing.eliminate_enums import eliminate_enumerations

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
        if alpha < 10:
            alpha = 10
        if alpha > 50:
            alpha = 50

        globals.ALPHA = alpha
        text = input_text
        # principal_character_name = get_principal_character_name(text)
        text = re.sub(r'[ \t]*-', '-', text)  # removing spaces before dialogue line
        text = re.sub(r'[ \t]+', ' ', text)  # removing multiple spaces / tab into a single space
        text = re.sub(r'([-*/_=+~`,.!;\'\"\\\[\]?])', r' \1 ',
                      text)  # adding a space before / after every non alfa numeric character
        # just so it can't be taken into account with a word (ex: car.Car => car . Car )
        text = re.sub(r'[ \t]+', ' ', text)  # reducing spaces and tab to single space
        text = re.sub(r'[\n]+', '\n', text)  # eliminating multiple endlines

        # TODO: CALCUALTE WORD SCORES HERE

        text, alpha = remove_dialog(text, alpha)
        if alpha >= 100:
            return text, None

        text = eliminate_enumerations(text)

        # TODO: CALCULAT SCORUL CUVINTELOR DIN TEXT

        # Product sentence scores
        sent2score = defaultdict(lambda: 0)

        paragraphs = str.splitlines(text)
        # set_max_score_sentence_with_best_name(principal_character_name, paragraphs, sent2score)
        #set_max_score_sentence_with_best_name(principal_character_name, paragraphs, sent2score)
        # todo: decomment this after polyglot is installed
        for paragraph in paragraphs:
            if paragraph == " " or paragraph == "":
                continue
            sentences = nltk.sent_tokenize(paragraph)
            paragraph_score = 0

            # calculate Sentences scores
            for sentence in sentences:
                for word in nltk.word_tokenize(sentence.lower()):
                    sent2score[sentence] += globals.SCORES[word]
                    if sentence not in sent2score.keys():
                        # sent2score[sentence] = get_word_score(word)
                        # TODO: FIX THIS HERE AFTER TEXT IS ANALYSED
                        sent2score[sentence] = randrange(10)
                    else:
                        sent2score[sentence] += randrange(10)
                        # sent2score[sentence] += get_word_score(word)
            # calculate Sentences scores

            for sentence in sentences:
                if sentence in sent2score.keys():
                    paragraph_score += sent2score[sentence]

            # calculate paragrahpes scores
            for sentence in sentences:
                if sentence in sent2score.keys():
                    sent2score[sentence] += int(PARAGRAPH_UPDATE_CONSTANT * paragraph_score)

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


if __name__ == '__main__':
    process_text("""
   -        Acasa e bine.
Cristi doarme,e vesel si n  - a facut ce trebuie.


s - a auzit un bum. Acasa este frig.
Afara ninge.
""", 50)
