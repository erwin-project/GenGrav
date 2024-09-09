import re
import io
import time
import random
import requests
import string
import spacy
import nltk
from nltk.stem import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from googletrans import Translator

nltk.download("stopwords")

# URL_API = ("https://api-inference.huggingface.co/models/google-bert/"
#            "bert-large-uncased-whole-word-masking-finetuned-squad")
URL_API = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"
headers = {"Authorization": "Bearer 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"}


def CheckScore(value):
    if value['score'] < 0.001:
        return ''
    else:
        return value['answer']


def CheckCoordinate(data_coordinate):
    if (data_coordinate['north'] > data_coordinate['south']) and (data_coordinate['west'] < data_coordinate['east']):
        return True
    else:
        return False


def GeneratorMessage(response):
    for word in response.split():
        yield word + " "
        time.sleep(0.05)


def CheckCache(cache, target):
    for key, val in target.items():
        if not (cache[key] != '' and val == ''):
            cache[key] = val
        else:
            target[key] = cache[key]

    return cache, target


def CheckParamMessage(**kwargs):
    params_none = [key for key, val in kwargs.items() if val is None or val == '']

    if len(params_none) != 0:
        list_param = ', '.join(params_none)
        message = f'Please provide the data information about {list_param}'
    else:
        message = ''

    return params_none, message


def ConvertDataDownload(data):
    # Convert DataFrame to CSV
    csv_buffer = io.StringIO()
    data.to_csv(csv_buffer, index=False)
    csv_data = csv_buffer.getvalue()

    return csv_data


def GetNumberUnique(lst):
    """Generate a random number within a range that is not in the given list."""
    if not lst:
        # If the list is empty, any number within the range is valid
        return random.randint(1, 1000000)

    while True:
        rand_num = random.randint(1, 1000000)

        if rand_num not in lst:
            return rand_num


def query(payload):
    response = requests.post(URL_API, headers=headers, json=payload)

    return response.json()


def CleanText(text, stem='Stem'):
    # Create a Translator object
    translator = Translator()

    # Translate the text to English
    translated = translator.translate(text, dest='en')

    # Make lower
    text = text.lower()

    # Remove line breaks
    # Note: that this line can be augmented and used over
    # to replace any characters with nothing or a space
    text = re.sub(r'\n', '', text)

    # # Remove punctuation
    # translator = str.maketrans('', '', string.punctuation)
    # text = text.translate(translator)

    # Remove stop words
    text = text.split()
    useless_words = nltk.corpus.stopwords.words("english")
    useless_words = useless_words + ['hi', 'im']

    text_filtered = [word for word in text if not word in useless_words]

    # # Remove numbers
    # text_filtered = [re.sub(r'\w*\d\w*', '', w) for w in text_filtered]

    # Stem or Lemmatize
    if stem == 'Stem':
        stemmer = PorterStemmer()
        text_stemmed = [stemmer.stem(y) for y in text_filtered]
    elif stem == 'Lem':
        lem = WordNetLemmatizer()
        text_stemmed = [lem.lemmatize(y) for y in text_filtered]
    else:
        text_stemmed = text_filtered

    final_string = ' '.join(text_stemmed)

    return final_string
