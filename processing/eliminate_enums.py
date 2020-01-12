import re
import nltk
import heapq
import traceback
from rippletagger.tagger import Tagger
from collections import Counter
from text_processor import assign_score_to_words
from text_processor import process_text
import text_processor

text1 = open(r'../input_examples/Automobilul.txt')
text2 = open(r'../input_examples/Avionul.txt')
text3 = open(r'../input_examples/GradinaFermecata.txt')
text4 = open(r'../input_examples/Incalzirea_globala.txt')
text5 = open(r'../input_examples/Mihai_Eminescu.txt')


def eliminate_enumerations(sentences, scores = {}):
    """
    This function eliminates enumerations from sentences
    :param sentences: the output from @process_text
    :param scores: the output from @assign_score_to_words
    :return: dict: keys: sentences with the eliminated enumerations if it's the case
		     values: for each sentence, the word that had the highest score or None if no enumeration was found
    """
    enum_regexp = re.compile(r"((\w+\-?\w+\s*\,\s*){2,100}\w+\-?\w+)|((\w+\-?\w+\s*\,\s*){1,100}\s*\w+\s+(si)\s+\w+)")
    enum_regexp_special_case = re.compile(r"((\w+\-?\w+\s*\,\s*){2,100})")
    tagger = Tagger(language="ro")
    tagged_sentences = tagger.tag(sentences[0])

    # todo: process the text into sentences if the input is changed
    # list of strings
    sentences = sentences[0].split('\n\n')

    # finding the enumerations
    enumerations = list()
    for sentence in sentences:
        sent_enums = [enum_regexp.findall(sentence), enum_regexp_special_case.findall(sentence)]
        enumerations.append(sent_enums)

    # process the findall output and take only the full_match enum
    for i in range(0, len(enumerations)):
        if enumerations[i][0]:
            max_len = max([len(j) for j in enumerations[i][0][0]])
            max_len_index = [j for j in range(0, len(enumerations[i][0][0])) if len(enumerations[i][0][0][j]) == max_len][0]
            enumerations[i][0] = enumerations[i][0][0][max_len_index]

        if enumerations[i][1]:
            max_len = max([len(j) for j in enumerations[i][1][0]])
            max_len_index = [j for j in range(0, len(enumerations[i][1][0])) if len(enumerations[i][1][0][j]) == max_len][0]
            enumerations[i][1] = enumerations[i][1][0][max_len_index]

    # split the enumerations into tokens of words in tokenized_enums
    tokenized_enums = list()
    token_regex = re.compile(r"\w+-?\w*")
    for it in enumerations:
        if it != [[], []]:
            tokenized_enum = [token_regex.findall(str(it[0])), token_regex.findall(str(it[1]))]
            tokenized_enums.append(tokenized_enum)
        else:
            tokenized_enums.append([[], []])

    # the output dictionary
    no_enum_sen_wscore = dict()

    # for each enumeartion
    for enumeration in range(0, len(enumerations)):

        # if they are not null
        if enumerations[enumeration] != [[], []]:

            # call the function that outputs the part of speech
            p_o_speech = get_part_of_speech_enum(tagged_sentences, tokenized_enums[enumeration][0])

            # check if the words from each enumeartion are NOUN, ADJ or ADV
            count = 0
            for enum_word in p_o_speech:
                if enum_word[1] == 'NOUN' or enum_word[1] == 'ADJ' or enum_word[1] == 'ADV' or enum_word[0].lower() == 'și':
                    count += 1

            # if they are then eliminate the enum from the sentence and put it in output dictionary
            if count == len(p_o_speech):
                # todo: cand primesc dictionarul cu scorurile, se va alege cuvantul cu scorul maxim din p_o_speech
                no_enum_sen_wscore[sentences[enumeration].replace(enumerations[enumeration][0], '')] = p_o_speech[0][0]

            # do the same thing again for the special case if the regular case didn't match
            else:
                if tokenized_enums[enumeration][1]:
                    p_o_speech_special_case = get_part_of_speech_enum(tagged_sentences, tokenized_enums[enumeration][1])
                    count = 0
                    for enum_word in p_o_speech_special_case:
                        if enum_word[1] == 'NOUN' or enum_word[1] == 'ADJ' or enum_word[1] == 'ADV' or enum_word[0].lower() == 'și':
                            count += 1

                    # daca este enumeratie cs ce trebuie eliminata
                    if count == len(p_o_speech_special_case):
                        # todo: cand primesc dictionarul cu scorurile, se va alege cuvantul cu scorul maxim din p_o_speech_special_case
                        no_enum_sen_wscore[sentences[enumeration].replace(enumerations[enumeration][1], '')] = p_o_speech_special_case[0][0]

        # if they are null then append to the key sentence the None value
        else:
            no_enum_sen_wscore[sentences[enumeration]] = None

    return no_enum_sen_wscore


def get_part_of_speech_enum(tagged_sentences, tokenized_enum):
    """
    This function takes the elements of an enumeration and assigns them the part of speech based on the most common part_of_speech
    found for that element, from all sentences
    :param tagged_sentences: list of tuples containing each word found in text paired with a part_of_speech
    :param tokenized_enum: list of words
    :return: list of list pairs that contains the words from tokenized_enum paired with it's part_of_speech based on sentences' majority
    """
    token_regex = re.compile(r"\w+-?\w*")
    part_of_speech_enum = []
    for elem in range(0, len(tokenized_enum)):
        part_of_speech = []
        for it in tagged_sentences:
            if it[1] not in ["PUNCT", "", "NUM", "SYM"]:
                if token_regex.findall(it[0])[0].lower() == tokenized_enum[elem].lower():
                    part_of_speech.append(it[1])
        dict_occur_pospeech = Counter(part_of_speech).most_common(1)[0]
        part_of_speech_enum.append([tokenized_enum[elem], dict_occur_pospeech[0]])
    return part_of_speech_enum

# # Test
# texts = [process_text(text1.read(), 0), process_text(text2.read(), 100), process_text(text4.read(), 0), process_text(text5.read(), 0)]
# for text in texts:
#     ret_dict = eliminate_enumerations(text)
#     print("New text:")
#     for it in ret_dict.items():
#         if it[1] is not None:
#             print(it[0], ":", it[1])
# print(text_processor.assign_score_to_words(text_processor.find_singularity(texts[0][0])[0]))





