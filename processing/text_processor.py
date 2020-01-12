import re
import nltk
import copy
import heapq
import pprint
import traceback
import googletrans

from rippletagger.tagger import Tagger
from nltk.corpus import stopwords
from gensim.models import Word2Vec
from pattern3.text import singularize


# nltk.download('punkt')


def assign_score_to_words(words):
    """
    Function that assigns a specific score to words based on their sentence parts
        proper noun = +4 score
        noun = +2 score
        verb = +2 score
        other = +1 score

    :param words: a dictionary for the words, where keys are the word in romanian and words[key] is the information
        about the respective word (output from 'find_singularity' function)

    :return: dictionary where each pair (key, value) will be (word, score_of_word)
    """

    scores = {
        "PROPN": 4,
        "NOUN": 2,
        "VERB": 2,
        "OTHER": 1
    }

    words_copy = {}
    tagger = Tagger(language='ro')
    for word in words.keys():
        info = tagger.tag(word)[0]
        part_of_sentence = info[-1]

        if part_of_sentence in scores.keys():
            words_copy[word] = scores[part_of_sentence] * words[word]['count']
        else:
            words_copy[word] = scores['OTHER'] * words[word]['count']

    return words_copy


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

    word_trans = googletrans.Translator()

    stop_words = nltk.corpus.stopwords.words('romanian')
    word2count = {}
    dictionary_text = []
    count_sentence = 0
    for sentence in nltk.sent_tokenize(input_text):
        count_sentence += 1
        sentence_words = []
        for _word in nltk.word_tokenize(sentence):
            _word = _word.lower()
            if _word not in stop_words:
                sentence_words.append(_word)
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
    input_text = """A fost odată o mică ciobăniță numită Margareta. Părinții ei se stinseseră cu mulți ani în urmă și, ca să nu moară de foame,
un unchi o luase pe copilă să o crească în casa lui. După ce copila se făcu ceva mai mare, unchiul acela îi dete în grijă o turmă de
oi și îi zise să le ducă pe deal la păscut. Mieii și oile săreau de colo-colo și mâncau pe săturate, dar Margareta trebuia să bage bine
de seamă să nu se piardă vreuna. Dar iată că într-o zi, un lup mare dădu iama în turmă și când oile văzură dihania setoasă de
sânge fugiră care încotro, fără urmă. Când Margareta văzu isprava lupului, se puse pe un plâns amarnic. Se întoarse totuși la casa
unchiului tremurând ca varga de frică. Unchiul ei era un om aspru și dintr-o bucată și fata știa că o să fie vai și amar când va
apărea fără oi.
- Unde e turma?, o întrebă el pe fată când o văzu venind către casă.
Margareta îi povesti repede ce se întâmplase, dar unchiul se cătrăni așa de tare cum fata nu mai pomenise niciodată în viața ei. La
început o certă și îi spuse că era leneșă și nepricepută. Dar cu cât se aprindea mai tare, cu atât creștea și mânia lui. Așa că o
prinse pe Margareta de părul ce-i atârna pe spate într-o coadă neagră și lungă și o trase la pământ în felul cel mai crud cu putință.
Dar nici așa nu fu mulțumit. Se duse în curte și aduse un băț cu care o bătu zdravăn, iar biata fată plângea de se scutura cămașa
pe ea.
- Unchiule, unchiule, țipa ea, cu ce sunt eu de vină că lupul a dat iama în oi? Dar bărbatul cel crud nu cunoștea mila.
- Să pleci din casa mea, strigă el în cele din urmă, ostenit de atâta bătaie, că nici nu putea să mai sufle. Să te duci de aici și
să nu te mai întorci până ce nu-mi aduci oile înapoi!
Margareta plecă grabnic și, deși nu știa încotro mergea, era bucuroasă că scăpase dintr-un asemenea loc, cu un om așa de lipsit
de inimă. Copila fugi drept în pădure, însă aceasta era atât de departe că ajunse acolo mai mult moartă decât vie de oboseală. Se
așeză sub un copac mare și începu să se gândească la ce avea de făcut. „Of, unchiule, unchiule!” începu ea să se tânguie „De ce
m-ai bătut așa de tare fără să am vreo vină? Ce-ar spune măicuța mea dacă ar ști ce viață grea îndur eu de când ea nu mai este? 
Și acum ce-o să fac? N-am nici casă, nici prieteni, nici de mâncare. Fără îndoială că voi muri de foame în pădurea asta în care nu
am nici ce mânca, nici adăpost.” Și uite-așa se tânguia întruna biata Margareta. Copacul cel înalt de lângă ea își scutură coroana
de frunze grele încoace și încolo și își murmură și el mila printr-un foșnet adânc. Chiar și firele de iarbă de la picioarele ei începură
să pălească și să se ofilească când auziră plânsetele și suspinele îndurerate ce veneau de pe buzele fetei.
Deodată, ajunse la urechile Margaretei un zgomot de pași ușori și, ridicând ochii, fata văzu apropiindu-se o femeie frumoasă
ce venea dintre copaci. La început copila se temu și se ridică să fugă. Dar tocmai atunci făptura cea ciudată spuse:
"""
    # elupoae
    output = find_singularity(input_text)

    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(output[0])
    print(output[1])

    vocabulary = Word2Vec(output[1], min_count=1, size=100, window=5, sg=0)
    print(vocabulary.wv.vocab.keys())


