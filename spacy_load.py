import spacy
from pathlib import Path
import getpass

username = getpass.getuser()

spacy_path = Path('C:\\Users\\{}\\AppData\\Local\\pypoetry\\Cache\\virtualenvs\\hw-12-nlp-lTN8LurM-py3.11\\Lib\\site-packages\\en_core_web_sm-3.7.1.dist-info'.format(username))

if not spacy_path.exists():
    spacy.cli.download("en_core_web_sm")
nlp = spacy.load('en_core_web_sm')
