"""Multilingual Online Translator Module"""

import re

import requests
from bs4 import BeautifulSoup


class Translator:
    """A simple translator class."""

    languages = {
        "en": "English",
        "fr": "French"
    }

    def __init__(self, language: str, word: str):
        self.language = language
        self.word = word
        self._response = self._get_response()

    def _get_query_url(self):
        """Construct the query URL based on the language and word."""

        host = "https://www.linguee.com"
        direction = ""

        if self.language == "en":
            direction = "french-english"
        elif self.language == "fr":
            direction = "english-french"
        else:
            raise ValueError("Unsupported language. Use 'en' for English or 'fr' for French.")

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
        examples = div_examples.find_all('a', class_='dictLink')

        div_featured = soup.find('div', class_='example line')
        try:
            examples_featured = div_featured.find_all('span', class_=re.compile('^tag_[ts]$'))
        except AttributeError:
            examples_featured = []
        examples.extend(examples_featured)
        return [example.text for example in examples]


def get_translator() -> Translator:
    """Prompt the user for translation language and word, and return a Translator instance."""

    print(
        "Type \"en\" if you want to translate from French into English, "
        "or \"fr\" if you want to translate from English into French:")
    language = input()
    print("Type the word you want to translate:")
    word = input()
    print(f"You chose \"{language}\" as a language to translate \'{word}\' to.")
    return Translator(language, word)


def main():
    tr = get_translator()
    print_translations(tr)


def print_translations(tr: Translator):
    """
    Print translations and examples from the response.

    :param tr: Translator object to get the translations and examples from
    """

    # print translation
    lang = Translator.languages[tr.language]
    print(f"{lang} Translations:")
    translations = tr.get_translations()
    for t in translations:
        print(t)

    # print examples
    print(f"\n{lang} Examples:")
    examples = tr.get_examples()
    for i in range(len(examples)):
        print(examples[i])
        if i % 2 != 0:
            print()


if __name__ == "__main__":
    main()
