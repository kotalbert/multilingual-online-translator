"""Multilingual Online Translator Module"""

import re

import requests
from bs4 import BeautifulSoup


class Translator:
    """A simple translator class."""

    languages = {
        '1': 'german',
        '2': 'english',
        '3': 'spanish',
        '4': 'french',
        '5': 'japanese',
        '6': 'dutch',
        '7': 'polish',
        '8': 'portuguese',
        '9': 'romanian',
        '10': 'russian',
    }

    def __init__(self, lang_from: str, lang_to: str, word: str):
        self.lang_from = lang_from
        self.lang_to = lang_to
        self.word = word
        self._response = self._get_response()

    def _get_query_url(self):
        """Construct the query URL based on the language and word."""

        host = "https://www.linguee.com"
        direction = f"{self.lang_from}-{self.lang_to}"

        return f"{host}/{direction}/search?query={self.word}"

    def _get_response(self) -> requests.Response:
        """Send a GET request to the constructed URL and return the response."""

        url = self._get_query_url()
        headers = {'User-Agent': 'Mozilla/5.0 AppleWebKit/537.36 Chrome/93.0.4577.82 Safari/537.36'}
        response = requests.get(url, headers=headers)
        if response.ok:
            print("200 OK")
        else:
            response.raise_for_status()
        return response

    def get_translations(self) -> list[str]:
        if self._response is None:
            self._get_response()
        soup = BeautifulSoup(self._response.text, 'html.parser')
        div_translation = soup.find('div', class_='translation_lines')
        translations = div_translation.find_all('a', class_='dictLink')
        return [translation.text for translation in translations]

    def get_examples(self) -> list[str]:
        if self._response is None:
            self._get_response()
        soup = BeautifulSoup(self._response.text, 'html.parser')
        div_examples = soup.find('div', class_='example_lines inexact')
        try:
            examples = div_examples.find_all('a', class_='dictLink')
        except AttributeError:
            examples = []

        div_featured = soup.find('div', class_='example line')
        try:
            examples_featured = div_featured.find_all('span', class_=re.compile('^tag_[ts]$'))
        except AttributeError:
            examples_featured = []
        examples.extend(examples_featured)
        return [example.text for example in examples]


def get_translator() -> Translator:
    """Prompt the user for translation language and word, and return a Translator instance."""

    print("Hello, welcome to translator. Translator supports:")
    for key, value in Translator.languages.items():
        print(f"{key}. {value.capitalize()}")

    print("Type the number of your language:")
    lang_from = input()
    lang_from = Translator.languages.get(lang_from, 'english')

    print("Type the number of language you want to translate to:")
    lang_to = input()
    lang_to = Translator.languages.get(lang_to, 'english')

    print("Type the word you want to translate:")
    word = input()

    return Translator(lang_from, lang_to, word)


def main():
    tr = get_translator()
    print_translations(tr)


def print_translations(tr: Translator):
    """
    Print translations and examples from the response.

    :param tr: Translator object to get the translations and examples from
    """

    # print translation
    print(f"{tr.lang_to} Translations:")
    translations = tr.get_translations()
    for t in translations:
        print(t)

    # print examples
    print(f"\n{tr.lang_to} Examples:")
    examples = tr.get_examples()
    for i in range(len(examples)):
        print(examples[i])
        if i % 2 != 0:
            print()


if __name__ == "__main__":
    main()
