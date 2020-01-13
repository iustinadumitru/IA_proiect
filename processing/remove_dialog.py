import re
from rippletagger.tagger import Tagger
from processing.globals import word_to_english
from processing.globals import scores
from processing.globals import word_score
from processing.globals import get_hashed_english_word
from processing.globals import add_word_to_english_dict
from processing.text_processor import find_singularity
from processing.translator import Translator


def clean_pre_text(text):
    first_non_whitespace_position = 0
    while text[first_non_whitespace_position] in [" ", "\n", "\t"]:
        first_non_whitespace_position += 1
    text = text[first_non_whitespace_position:]
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'[\n]+', '\n', text)
    text = re.sub(r'-[ \t]*', '-', text)
    text = re.sub(r'[.]', ' .', text)
    #print(text.lower())
    return text.lower()


def remove_dialog(text, alpha):
    text = re.sub(r'[ \t]*-', '-', text)
    final_text = ""
    i = 0
    while i < len(text):
        if i == 0 and text[i] == "-":
            while i < len(text) and text[i] != '\n':
                i += 1
        elif text[i] == "-" and text[i - 1] == "\n":
            while i < len(text) and text[i] != '\n':
                i += 1
        else:
            final_text += text[i]
            i += 1

    temp_text = clean_pre_text(text)
    tagger = Tagger(language="ro")
    original_len = len(temp_text)
    paragraphs = str.splitlines(temp_text)
    word_multiple_tags = dict()
    for paragraph in paragraphs:
        if paragraph == " " or paragraph == "":
            continue
        first_non_whitespace_position = 0
        while first_non_whitespace_position < len(paragraph) and paragraph[first_non_whitespace_position] in [" ", "\n", "\t"]:
            first_non_whitespace_position += 1
        paragraph = paragraph[first_non_whitespace_position:]
        if paragraph[0] != "-":
            continue
        #print("-------------")
        paragraph = paragraph[1:]
        paragraph = re.sub(r'[-]', ' ', paragraph)
        temp_tags = tagger.tag(paragraph)

        add_words_using_class(paragraph)
        #TODO: DECOMMENT THIS AND TEST IT BEFORE PROD RELEASE

        right_tags = []
        for it in temp_tags:
            if it[1] not in ["PUNCT", ""]:
                right_tags.append(it)
        for word, tag in right_tags:
            if word not in word_multiple_tags.keys():
                word_multiple_tags[word] = dict()
            if tag not in word_multiple_tags[word].keys():
                word_multiple_tags[word][tag] = 1
            else:
                word_multiple_tags[word][tag] += 1

    word_tag = dict()
    for word, tags_and_nr in word_multiple_tags.items():
        nr_max = 0
        nr_total = 0
        real_tag = "CONJ"
        for tag, nr in tags_and_nr.items():
            nr_total += nr
            if nr > nr_max:
                nr_max = nr
                real_tag = tag
        word_tag[word] = (real_tag, nr_total)

    #print(word_multiple_tags)
    #print("-------")
    #print(word_tag)
    for word, tag_nr in word_tag.items():
        tag = tag_nr[0]
        nr = tag_nr[1]
        update_dict(word, tag, nr)
    new_len = len(final_text)
    dialog_len = original_len - new_len
    alpha_dialog_cut = dialog_len * 1.0 / original_len * 100
    if int(alpha_dialog_cut) >= 99 - alpha or alpha_dialog_cut >= 100:
        new_alpha = 101
    else:
        new_alpha = int(100 * alpha / (100 - alpha_dialog_cut))
    return final_text, new_alpha

def add_words_using_class(paragraph):
    print(paragraph)
    paragraph += "."
    word_list = list()
    word = ""
    for letter in paragraph:
        if letter.isalpha():
            word += letter
        else:
            word_list.append(word)
            word = ""
    #TODO: TEST THIS AFTER FIND_SINGULARITY WORKS CORRECTLY
    translator = Translator()
    local_word_to_en = find_singularity(paragraph)
    if local_word_to_en:
        for it in local_word_to_en.items():
            if it[0].lower() not in word_to_english.keys():
                add_word_to_english_dict(it[0], it[1])


def update_dict(word, tag, count):
    eng_word = get_hashed_english_word(word)
    if eng_word == "WORD NOT FOUND IN DICT!!":
        return
    if tag in scores.keys():
        if eng_word in word_score.keys():
            word_score[eng_word] += scores[tag] * count
        else:
            word_score[eng_word] = scores[tag] * count
    else:
        if eng_word in word_score.keys():
            word_score[eng_word] += scores["OTHER"] * count
        else:
            word_score[eng_word] = scores["OTHER"] * count

if __name__ == '__main__':
    print(remove_dialog("""-piata pietei pietelor Piata si au mers si au corectat chestii. Masina a mers foarte bine afara.
                paragraf cu caractere dubioase:`'][:}{.
                Acesta este un cuvant normal, iar acesta nu.
                -Alt dialog incepe aici.""", 1))
    exit(99)
    print(remove_dialog("""
    -pisicilor pisicile Germania a ajuns acasa. A avut nevoie de o geanta.
    -Primul automobil, construit de inginerul german Karl Benz in anul 1885, s-a numit Motorwagen si era vehicul propulsat de un motor cu explozie in patru timpi, alimentat cu benzina.
    
    -Pentru a porni, motorul trebuia incalzit mai intai cu apa fierbinte, iar apoi, in timp ce soferul manevra pornirea, vehiculul trebuia impins pana cand pistoanele ajungeau sa functioneze singure.
    
    -Benz si-a prezentat oficial inventia in public la 3 iulie 1886, pe Ringstrasse din Mannheim, iar la demonstratie s-a produs si un incident nefericit.
    
    -Motorwagen era alimentat cu benzina, iar acest lucru a alarmat opina publica, pentru ca tocmai in acele vremuri aparusera masinile de gatit cu petrol, care mai faceau explozie prin bucatarii.
    
    -Inginerul Benz nu s-a descurajat si a prezentat noi modele mai silentioase si a propus amenajarea unor statii de alimentare cu benzina la unele intersectii, pentru ca rezervorul masinii sa nu fie prea mare.
    
    -Pentru a populariza inventia sotului ei, Bertha Benz a luat Patent-Motorwagen nr 3, se spune fara stirea lui Karl, si a plecat cu automobilul sa-si viziteze rudele, pentru a-i demonstra utilitatea ca mijloc de transport pe distante lungi.
    
    -Excursia a inceput la inceputul lunii august 1888, iar intreprinzatoarea doamna si-a luat la bord si cei doi fii, pe Eugen si Richard, si au calatorit din Mannheim, prin Heidelberg si Wiesloch, pana in Pforzheim, orasul natal.
    
    -Pe langa a fi sofer, Bertha Benz a fost si mecanic, curatind pe drum carburatorul cu un ac de palarie si folosind o jartiera pentru a izola un cablu.
    
    -In Germania, pentru a celebra acesata calatorie, la fiecare doi ani este organizata o parada a automobileleor de epoca, iar in 2008, Ruta Memoriala Bertha Benz a fost aprobata oficial ca ruta a mostenirii industriale a realizarilor umane.
    
    """, 50))
    exit(99)

    print(remove_dialog("""
        Acasa ploua ieri.
        - Casa casei caselor erau verzi.
        """, 2))

