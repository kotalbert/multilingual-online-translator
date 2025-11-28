"""Multilingual Online Translator Module"""

import re

import requests
from bs4 import BeautifulSoup


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
            direction = "english-french"
        elif self.language == "fr":
            direction = "french-english"
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
    if response.ok:
        print("200 OK")
    else:
        response.raise_for_status()
    print("Translations")
    soup = BeautifulSoup(response.text, 'html.parser')

    # print translation
    translations = soup.find_all('a', class_='dictLink')
    trans_texts = [translation.text for translation in translations]
    print(trans_texts)

    # print context
    contexts_to = soup.find_all('span', class_='tag_t')
    contexts = soup.find_all('span', class_=re.compile(r'tag_[ts]$'))
    context_texts = [context.text for context in contexts]
    print(context_texts)



if __name__ == "__main__":
    main()
