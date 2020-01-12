import pprint
import re

import googletrans

from processing.translator import Translator
import nltk
from gensim.models import Word2Vec
from pattern3.text import singularize
from rippletagger.tagger import Tagger


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

    #word_trans = Translator() ??
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

def translate_words(input_text):
    """
    :param input_text: original text
    :return: word
             word dictionary like: {"word": "word_in_en"}
    """

    #word_trans = Translator() ??
    word_trans = googletrans.Translator()
    stop_words = nltk.corpus.stopwords.words('romanian')
    word2count = {}
    count_sentence = 0
    for sentence in nltk.sent_tokenize(input_text):
        count_sentence += 1
        sentence_words = []
        for _word in nltk.word_tokenize(sentence):
            if _word not in stop_words:
                sentence_words.append(_word)
                if _word not in word2count.keys():
                    word_in_en = word_trans.translate(_word, "en").text
                    word_in_en = singularize(word_in_en)
                    word2count[_word] = word_in_en

    print("Finish to process: {} sentences".format(count_sentence))
    return word2count


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
