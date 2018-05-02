import math
import re

from newspaper import Article, Source

from src.repo import Repo, lower
from src.models import Official

AVERAGE_WPM = 250


def parse_publisher(url):
    source = Source(url, memoize_articles=False)
    source.build()
    print(f'Done building source: {url}')
    return [article.url for article in source.articles]


def parse_article(html):
    article = Article(url='http://')
    article.download_state = 'done'
    article.html = html
    article.parse()
    return {
        'title': article.title,
        'authors': article.authors,
        'date_published': article.publish_date,
        'text': article.text,
        'top_image_url': article.top_image,
        }


def classify(text):
    classification = None
    text = text.lower()
    names = extract_full_official_names(text)
    for name in names:
        name = ' '.join(name)
        if text.find(name) != -1:
            classification = 'political'
            break
    return classification


def calculate_read_time(text):
    """Calculates the average reading time of text in minutes rounded up."""
    word_count = len(text.split(' '))
    time = math.ceil(word_count / AVERAGE_WPM)
    return time or 1


def extract_summary_and_keywords(text, title):
    """Uses newspaper.Article NLP method to get a summary and keywords."""
    article = Article(url='http://', title=title)
    article.download_state = 'done'
    article.is_parsed = True
    article.text = text
    article.nlp()
    return article.summary, article.keywords


def mentioned_officials(text):
    officials = {}
    for full_name, count in extract_full_official_names(text).items():
        official = query_official(full_name)
        if official:
            officials[str(official.id)] = count
    return officials


def extract_full_official_names(text):
    text = text.lower()
    mapping = last_name_to_first_names_mapping()
    words = re.split(r'\W', text)
    full_names = {}
    for index, current_word in enumerate(words):
        first_names = mapping.get(current_word, False)
        if first_names:
            previous_word = words[index-1]
            if previous_word in first_names:
                full_name = (previous_word.lower(), current_word.lower())
                count = full_names.get(full_name, 0)
                full_names[full_name] = count + 1
    return full_names


def last_name_to_first_names_mapping():
    repo = Repo(Official)
    officials = repo.select('first_name', 'last_name')
    mapping = {}
    for official in officials:
        first_name = official.first_name.lower()
        mapping.setdefault(official.last_name.lower(), []).append(first_name)
    return mapping


def query_official(full_name):
    condition = official_condition(full_name)
    try:
        return Official.select().where(*condition)[0]
    except IndexError:
        print(f'Official not found: {full_name}')


def official_condition(full_name):
    first_name, last_name = full_name
    return (lower(Official.first_name) == first_name,
            lower(Official.last_name) == last_name)
