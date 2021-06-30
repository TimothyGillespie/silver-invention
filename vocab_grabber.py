import re
import sys

def is_german(text):
    return any([(x > u'\u0045' and x < u'\u00DF') for x in text])

def get_vocab_struct(text):
    preprocessed = re.split("(\.|\n)", text)

    preprocessed = [re.sub("\d", "", x).strip() for x in preprocessed]
    preprocessed = [x for x in preprocessed if x != "" and x != "."]

    defined_words = []
    examples = []
    translations = []

    word_part = True
    collection_german = []
    collection_korean = []

    previous_german = False

    for word in preprocessed:
        if word_part:
            if not is_german(word):
                word_part = False
            else:
                defined_words.append(word)

        if not word_part:
            if previous_german and not is_german(word):
                if len(collection_german) == 0:
                    examples.append("")
                else:
                    examples.append(";".join(collection_german))

                if len(collection_korean) == 0:
                    translations.append("")
                else:
                    translations.append(";".join(collection_korean))
                collection_korean = []
                collection_german = []

            if is_german(word):
                previous_german = True
                collection_german.append(word)
            else:
                collection_korean.append(word)


    result = zip(defined_words, translations, examples)
    return result


if __name__ == "__main__":

    with open(sys.argv[1], "r") as f:
        test = f.read()

    csv = ""
    csv += "word,translations,example\n"
    for (word, translation, example) in get_vocab_struct(test):
        csv += f'"{word}","{translation}","{example}"'
        csv += "\n"

    with open("output.csv", "w+") as f:
        f.writelines(csv)