from pathlib import Path
import textwrap


import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from spacy_load import nlp, username

from heapq import nlargest

"""python -m spacy download en_core_web_sm та додайте строку nlp = spacy.load('en_core_web_sm')
 Якщо при запуску main.py отримаєте
'OSError: [E050] Can't find model 'en_core_web_sm'.
 It doesn't seem to be a Python package or a valid path to a data directory.
'
"""


path_to_nltk = Path(f'C:\Users\{username}\AppData\Roaming\nltk_data')
if not path_to_nltk.exists():
    nltk.download('punkt_tab')
    nltk.download('stopwords')


def get_summary(source_text, number_of_sentence, library='spacy'):
    """
    A function to  generate and write to file a summary from a given source text based on word frequencies.

    Parameters:
    - source_text: the input text to generate the summary from
    - number_of_sentence: the number of sentences to include in the summary
    - library: the library(spacy or nltk) to use for text processing (default is 'spacy')

    Returns:
    - summary_collected: the generated summary text
    """

    #  Отримаємо токени слів та видаляємо пунктуацію з Spacy
    doc = nlp(source_text)
    tokens_spacy = [token.text for token in doc if not token.is_punct]

    # Отримаємо токени слів, речень та список stop_words з Nltk та видаляємо пунктуацію
    tokens_nltk = word_tokenize(source_text)
    filtered_tokens_nltk = [token for token in tokens_nltk if token.isalnum()]
    sentences = sent_tokenize(source_text)
    stop_words = set(stopwords.words('english'))

    # Оцінка важливості кожного слова spacy
    word_frequencies = {}
    if library == 'spacy':
        tokens = tokens_spacy
    elif library == 'nltk':
        tokens = filtered_tokens_nltk
    else:
        print('Supported only "spacy" and "nltk" libraries')

    for word in tokens:
        if word.lower() not in stop_words:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1

    # Оцінка важливості кожного речення
    sentence_scores = {}
    for sent in sentences:
        for token in nlp(sent):
            word = token.text.lower()
            if word in word_frequencies.keys():
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word]
                else:
                    sentence_scores[sent] += word_frequencies[word]

    # Вибір трьох найважливіших речень
    summary_sentences = nlargest(number_of_sentence, sentence_scores, key=sentence_scores.get)

    # Виведення підсумку
    summary_collected = ' '.join(summary_sentences)

    file_name = "summary_spacy.txt" if library == "spacy" else "summary_nltk.txt"

    with open(file_name, "w", encoding="utf-8") as f:
        f.write(textwrap.fill(summary_collected, width=80))

    return summary_collected


if __name__ == '__main__':
    with open("source.txt", "r") as file:
        text = file.read()

    # library = 'nltk'
    library = 'spacy'

    source_text = text.replace('\n', ' ')
    get_summary(text, 3, library)
