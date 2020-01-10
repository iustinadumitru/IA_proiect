"""
:author: Lupoae Eduard Valentin
"""
import re

from rippletagger.tagger import Tagger

dict_punct = {
    "...": "ELLIPSIS",
    "[...]": "ELLIPSIS",
    ".": "POINT",
    "?": "QMARK",
    "!": "EMARK",
    ":": "COLON",
    "-": "DIALOGUE"
}

dict_separator = {
    "...": "...###",
    "[...]": "[...]###",
    ".": ".###",
    "?": "?###",
    "!": "!###",
}


def text_separator():

    text_dict = {"paragraph": [],
                 "sentences": [],
                 "analyses": []}

    tagger = Tagger(language="ro")
    text_support = "Karl Benz dar nici așa Cristi , Marea Neagra nu fu mulțumit Motorwagen. Se duse în curte și aduse un băț cu care o bătu zdravăn, iar biata " \
                   "fată plângea de se scutura cămașa pe ea. - Unchiule, unchiule, țipa ea, cu ce sunt eu de vină că " \
                   "lupul a dat iama în oi? Dar bărbatul cel crud nu cunoștea mila. - Să pleci din casa mea, strigă " \
                   "el în cele din urmă, ostenit de atâta bătaie, că nici nu putea să mai sufle. Să te duci de aici " \
                   "și să nu te mai întorci până ce nu-mi aduci oile înapoi!"

    mrep = lambda s, d: s if not d else mrep(s.replace(*d.popitem()), d)

    text_support = re.sub(r'\s+', ' ', text_support)
    for sign in ['.', '!', '?', '...', '[...]', ':', "'", ',', '"']:
        text_support = str.replace(text_support, sign, " " + sign)

    # separa propozitiile in functie de semnele de punctuatie
    text_support = mrep(text_support, dict_separator).split("###")[:-1]

    text_support = [sentence[1:] if sentence[0] == " " else sentence for iterable, sentence in enumerate(text_support)]

    for sentence in text_support:
        text_dict["sentences"].append(sentence)
        text_dict["analyses"].append(tagger.tag(sentence))

    print(text_dict)


def remove_sentence():
    pass


def main():
    text_separator()


if __name__ == "__main__":
    main()
