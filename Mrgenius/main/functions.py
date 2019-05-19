
from django.shortcuts import get_object_or_404
from .models import WordList, Question
from bs4 import BeautifulSoup
from hazm import word_tokenize as h_word_tokenize, stopwords_list
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import collections
import requests
import difflib
import wikipedia


class CheckWord(object):

    @classmethod
    def search_wikipedia(cls, word):
        page = requests.get("https://fa.wikipedia.org/wiki/" + word)
        soup = BeautifulSoup(page.content, features="html.parser")

        word_tokenized = []
        try:
            size = len(soup.find_all('p'))
            content = soup.find_all('p')
            for i in range(size):
                word_tokenized.append(word_tokenize(content[i].get_text()))


            filtered_words = []
            for list in word_tokenized:
                for word in list:
                    if word not in stopwords_list():
                        if word.isalpha():
                            filtered_words.append(word)

            most_common_words = (collections.Counter(filtered_words).most_common(10))
            return most_common_words

        except:
            return "error"

    @classmethod
    def add_to_database(cls, word, question_id):
        word1 = word
        try:
            word1 = word.replace(" ", "_")
            most_common_words = cls.search_wikipedia(word1)
            most_common = most_common_words[0][1]
        except:
            most_common_words = cls.search_wikipedia(word)
            most_common = most_common_words[0][1]
        for w, n in most_common_words:
            question = get_object_or_404(Question, id=question_id)
            similarity_percent = (n * 90) / most_common
            WordList.objects.create(word=w, fk_question=question, similarity_percent=similarity_percent)
        return True

    @classmethod
    def wikipedia_summary(cls, word):
        wikipedia.set_lang("fa")

        summary = wikipedia.summary(word)
        summary = summary.replace(word, "*")
        summary = sent_tokenize(summary)

        return summary

    @classmethod
    def get_info(cls, word):
        page = requests.get("https://fa.wikipedia.org/wiki/" + word)
        soup = BeautifulSoup(page.content, features="html.parser")

        content = soup.find_all("table", {"class": "infobox vcard"})
        x = list(content[0].tbody)
        f = []
        l = []
        for i in x:
            try:
                f.append(i.td.get_text())
                l.append(i.th.get_text())
            except:
                f.append("error")
                l.append("error")

        result = []
        for i in range(len(f)):
            try:
                result.append("{}: {}".format(f[i + 1], l[i]))
            except:
                pass

        return result

    @classmethod
    def check_similarity(cls, word, answer):
        seq = difflib.SequenceMatcher(None, answer, word).ratio() * 100
        return seq



