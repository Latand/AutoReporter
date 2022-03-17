import random
import re

LANGUAGES = [
    'en',
    'ru',  # Увеличим вероятность выпадения языка
    'ru',
    'uk'
]


def load_channels(path=None):
    if not path:
        path = 'data/channels.txt'
    with open(path, 'r') as file:
        urls = file.read()
    return urls


def load_proxies(path=None):
    if not path:
        path = 'data/proxies.txt'
    with open(path, 'r') as file:
        proxies = file.readlines()
    return proxies


def get_valid_channel_urls(text):
    urls = re.findall(r'(?P<url>https?://[^\s]+)', text)
    usernames = re.findall(r'(@[^\s|()]+)', text)
    return urls + usernames


def get_random_language():
    return random.choice(LANGUAGES)
