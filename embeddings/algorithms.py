import re
from random import random


def negative_sampling(word2index, index2word, sentences, K=5):
    sampling = []
    for index, sentence in enumerate(sentences):
        print(index, '/', len(sentences))
        words = sentence2word(sentence)
        for i in range(len(words) - 1):
            current_word = words[i]
            target_word = words[i+1]
            sampling.append({'context': current_word, 'target_word': target_word, 'result': 1})
            for k in range(K):
                sampling.append({'context': current_word, 'target_word': index2word[int(random()*len(index2word))],
                                 'result': 0})


def glove(word2index, index2word, sentences):
    print('GloVe')


def sentence2word(sentence):
    """
    Converts sentence to list of words. Gets rid of non alphanumeric characters
    :param sentence: Sentence we wish to split
    :return: list of strings
    """
    return[re.sub('[^A-Za-z0-9]+', '', word) for word in sentence.replace("' ", "'").split(' ')]


def doc2sentence(doc):
    """
    Converts document with carriage returns to list of strings.
    :param doc: Document we wish to split
    :return: list of strings
    """
    sentences = doc.split('\n')
    sentences = list(filter(lambda sentence: sentence not in("", " ", "\n"), sentences))
    return sentences