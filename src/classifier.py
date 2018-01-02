import re
from nlp import Repo
from nlp.models import Official
# from nlp.analysis import extract_full_official_names


class Classifier:
    """Determine the category in which given text falls."""

    def __init__(self, text):
        self.classification = None
        self.classify(text.lower())

    def classify(self, text):
        names = extract_full_official_names(text)
        for name in names:
            name = ' '.join(name)
            if text.find(name) != -1:
                self.classification = 'political'
                break


def extract_full_official_names(text):
    mapping = last_name_to_first_names_mapping()
    words = re.split(r'\W', text)
    full_names = set()
    for index, current_word in enumerate(words):
        first_names = mapping.get(current_word, False)
        if first_names:
            previous_word = words[index-1]
            if previous_word in first_names:
                full_names.add((previous_word, current_word))
    return full_names


def last_name_to_first_names_mapping():
    repo = Repo(Official)
    officials = repo.select('first_name', 'last_name')
    mapping = {}
    for official in officials:
        first_name = official.first_name.lower()
        mapping.setdefault(official.last_name.lower(), []).append(first_name)
    return mapping
