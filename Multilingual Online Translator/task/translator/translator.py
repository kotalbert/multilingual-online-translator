"""Multilingual Online Translator Module"""


def main():
    display_menu()


def display_menu():
    print(
        "Type \"en\" if you want to translate from French into English, "
        "or \"fr\" if you want to translate from English into French:")
    language = input()
    word = input()
    print(f"You chose \"{language}\" as a language to translate \'{word}\' to.")


if __name__ == "__main__":
    main()
