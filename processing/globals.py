word_to_english = dict()
#this dictionary will register the translation of a word
#word_to_english["caine"] = "dog"

scores = {
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
