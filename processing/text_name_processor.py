import nltk
from polyglot.text import Text

from processing.globals import MAX_SCORE

male_singular_pronouns = ["el", "lui", "acestuia", "acesta", "acela", "dumnealui", "dansul", "dânsul", "domnul",
                          "domnisorul", "domnișorul", "domnisorului", "domnișorului", "lui"]
female_singular_pronouns = ["ea", "ei", "acesteia", "aceasta", "aceeea", "dumneaei", "dansa", "dânsa", "doamna",
                            "domnisoara", "domnișoara", "domnisoarei", "domnișoarei", "ei"]
male_plural_pronouns = ["ei", "acestia", "acestora", "aceia", "dansii", "dânsii", "domnii",
                          "domnisorii", "domnișorii", "domnisorilor", "domnișorilor"]
female_plural_pronouns = ["ele", "acestea", "acestea", "acelea", "dansele", "dânsele", "doamnele",
                          "domnisoarele", "domnișoarele", "domnisoarelor", "domnișoarelor"]
universal_singular_pronouns = ["eu", "tu", "mie", "tie", "dumneata", "dumneavoastra"]
universal_plural_pronouns = ["noi", "voi", "noua", "voua", "lor"]




# TODO: COMPLETE HERE

names_male_prev_statement = list()
names_female_prev_statement = list()
names_male_current_statement = list()
names_female_current_statement = list()
count_names = dict()

def get_principal_character_name(text):
    global names_male_prev_statement
    global names_female_prev_statement
    global names_male_current_statement
    global names_female_current_statement
    global count_names
    all_names = set()
    word = ""
    tag = Text(text, hint_language_code="ro").entities
    for it in tag:
        if it.tag == "I-PER":
            for name in it:
                all_names.add(name.lower())
    for letter in text:
        if letter.isalpha():
            word += letter
        else:
            word = word.lower()
            if word in all_names:
                if word not in count_names.keys():
                    count_names[word] = 1
                else:
                    count_names[word] += 1
                if word[len(word) - 1] == 'a': #female
                    names_female_current_statement.append(word)
                else:
                    names_male_current_statement.append(word)
            elif word in male_singular_pronouns:
                update_name_using_reference(0, False, names_male_current_statement, names_male_prev_statement)
            elif word in female_singular_pronouns:
                update_name_using_reference(1, False, names_female_current_statement, names_female_prev_statement)
            elif word in universal_singular_pronouns:
                update_name_using_reference(2, False, names_male_current_statement + names_female_current_statement,
                                            names_female_current_statement + names_male_current_statement)
            elif word in male_plural_pronouns:
                update_name_using_reference(0, True, names_male_current_statement, names_male_prev_statement)
            elif word in female_plural_pronouns:
                update_name_using_reference(1, True, names_female_current_statement, names_female_prev_statement)
            elif word in universal_plural_pronouns:
                update_name_using_reference(2, True, names_male_current_statement + names_female_current_statement,
                                            names_female_current_statement + names_male_current_statement)
            word = ""
        if letter == '.':
            if len(names_male_current_statement) > 0:
                names_male_prev_statement = names_male_current_statement.copy()
            if len(names_female_current_statement) > 0:
                names_female_prev_statement = names_female_current_statement.copy()
            names_male_current_statement = list()
            names_female_current_statement = list()

    max_count = -1
    return_name = ""
    for name, count in count_names.items():
        if count > max_count:
            max_count = count
            return_name = name
    return return_name


def update_name_using_reference(tag, is_plural, names_current, names_prev):
    global count_names
    found = False
    for name in reversed(names_current):
        count_names[name] += 1
        found = True
        if not is_plural:
            return
    if found:
        return
    for name in reversed(names_prev):
        count_names[name] += 1
        if not is_plural:
            return


def set_max_score_sentence_with_best_name(principal_character_name, paragraphs, sent2score):
    for paragraph in paragraphs:
        if paragraph == " " or paragraph == "":
            continue
        sentences = nltk.sent_tokenize(paragraph)

        for sentence in sentences:
            for word in nltk.word_tokenize(sentence.lower()):
                if word.lower() == principal_character_name:
                    sent2score[sentence] = MAX_SCORE
                    return

if __name__ == '__main__':
    t = r"Ana Maria Ana Maria merge la piata si cumpara o maria cuvant abstract mordor casa;."
    t2 = r"Cristi merge la piata. Afara ploua. El el el. Maria citeste si Maria scrie."
    t3 = r"Cristi merge. Ploua. El merge. Ploua. Maria merge. ei ei ei ei el si Ei merg. Andrei Andrei Andrei"
    sent2score = dict()
    print(get_principal_character_name(t3))
    set_max_score_sentence_with_best_name(get_principal_character_name(t3), str.splitlines(t3), sent2score)
    print(sent2score)


