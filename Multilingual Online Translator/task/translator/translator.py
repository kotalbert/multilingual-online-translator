"""Multilingual Online Translator Module"""

import requests
from bs4 import BeautifulSoup
from requests import Response


class Translator:
    """A simple translator class."""

    def __init__(self, language: str, word: str):
        self.language = language
        self.word = word

    def get_query_url(self):
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

    def get_response(self) -> requests.Response:
        """Send a GET request to the constructed URL and return the response."""

        url = self.get_query_url()
        headers = {'User-Agent': 'Mozilla/5.0 AppleWebKit/537.36 Chrome/93.0.4577.82 Safari/537.36'}
        response = requests.get(url, headers=headers)
        return response


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
    response = tr.get_response()
    print_translations(response)


def print_translations(response: Response):
    """
    Extract and print translations and examples from the response.

    :param response:
    """

    if response.ok:
        print("200 OK")
    else:
        response.raise_for_status()
    print("Translations")
    soup = BeautifulSoup(response.text, 'html.parser')

    # find translation
    div_translation = soup.find('div', class_='translation_lines')
    translations = div_translation.find_all('a', class_='dictLink')
    trans_texts = [translation.text for translation in translations]
    print(trans_texts)

    # find examples
    div_examples = soup.find('div', class_='example_lines inexact')
    examples = div_examples.find_all('a', class_='dictLink')
    examples_texts = [example.text for example in examples]
    print(examples_texts)


if __name__ == "__main__":
    main()
