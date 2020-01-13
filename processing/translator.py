import nltk
import time
import traceback
import urllib.parse
import urllib.request

from bs4 import BeautifulSoup


class TranslatorException(BaseException):
    def __init__(self, msg=""):
        super().__init__(msg)


class Translator:
    def __init__(self):
        self.LIMIT = 5000
        self.SITE = "http://translate.google.com/m?hl=%s&sl=%s&text=%s"
        self.HEADER = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'}

    def translate(self, text, source_lan='ro', dest_lan='en'):
        translated_text = ""
        request_text = ""
        request_size = 0

        sentences = nltk.sent_tokenize(text)
        nr_of_sentences = len(sentences)

        for index in range(len(sentences)):
            length_current_sentence = len(sentences[index])
            if request_size + length_current_sentence < self.LIMIT:
                request_size += length_current_sentence
                request_text += " " + (sentences[index])

                if index < nr_of_sentences - 1:
                    continue

            try:
                link = self.SITE % (dest_lan, source_lan, urllib.parse.quote(request_text))
                req = urllib.request.Request(link, headers=self.HEADER)

                page = urllib.request.urlopen(req)
                soup = BeautifulSoup(page, 'lxml')
                translated_text += " " + soup.find('div', {'dir': 'ltr'}).get_text()

                request_text = sentences[index]
                request_size = length_current_sentence

            except Exception as e:
                raise TranslatorException("Something went wrong while translating text, {}".
                                          format(traceback.format_exc()))

        return translated_text

    def translate_words(self, words, source_lan='ro', dest_lan='en'):
        nr_of_words = len(words)
        translated_words = ""
        request_words = ""
        request_size = 0

        for index in range(len(words)):
            current_size = len(words[index]) + 1

            if request_size + current_size < self.LIMIT:
                request_words += words[index] + "|"
                request_size += current_size

                if index < nr_of_words - 1:
                    continue

            try:
                link = self.SITE % (dest_lan, source_lan, urllib.parse.quote(request_words))
                req = urllib.request.Request(link, headers=self.HEADER)

                page = urllib.request.urlopen(req)
                soup = BeautifulSoup(page, 'lxml')
                translated_words += soup.find('div', {'dir': 'ltr'}).get_text()

                request_words = words[index]
                request_size = current_size

            except Exception:
                raise TranslatorException("Something went wrong while translating text, {}".
                                          format(traceback.format_exc()))

        translated_words = translated_words.split("|")
        translated_words = list(map(lambda x: x.lower().strip(), translated_words))
        return list(zip(words, translated_words))


if __name__ == '__main__':
    t = Translator()
    text = """"""
    words = nltk.word_tokenize(text)
    print(words)
    start = time.time()
    output = t.translate_words(words)
    end = time.time()

    print("1st translation:")
    print(output)
    print("Translated whole text in {} seconds".format(end - start))

    # start = time.time()
    # second_output = t.translate(output, source_lan='en', dest_lan='ro')
    # end = time.time()
    #
    # print("\n\n2nd translation:")
    # print(second_output)
    # print("Translated whole text in {} seconds".format(end - start))
    #
    # print(len(nltk.sent_tokenize(second_output)))
    # start = time.time()
    # for word in text.split(" "):
    #     t.translate(word)
    #
    # end = time.time()
    # print("Translated word by word in {} seconds".format(end - start))
