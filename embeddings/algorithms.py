import re
from random import random
import numpy as np
from keras.preprocessing.sequence import skipgrams, make_sampling_table


def negative_sampling(word2index, index2word, sentences, K=5):

    vocab_size = len(word2index)
    vector_dim = 300
    epochs = 1000000

    sentences = [[word2index[word] for word in sentence2word(sentence)] for sentence in sentences]
    print(sentences)

    validation_size = 16
    validation_window = 100
    validation_examples = np.random.choice(validation_window, validation_size, replace=False)

    sampling_table = make_sampling_table(vocab_size)
    couples, labels = [], []

    print('Creating skipgrams for ', len(sentences), "sentences")
    for index, sentence in enumerate(sentences):
        if index % 100 == 0:
            print('\r' + str(int(index*100/len(sentences))) + '%', end='')
        couple, label = skipgrams(sentences[0], vocab_size, window_size=validation_window, sampling_table=sampling_table)
        couples.extend(couple)
        labels.extend(label)

    word_target, word_context = zip(*couples)
    word_target = np.array(word_target, dtype="int32")
    word_context = np.array(word_context, dtype="int32")

    print([(index2word[i[0]], index2word[i[1]]) for i in couples[:10]], labels[:10])
    print('Couples:', len(couples))
    print('Labels:', len(labels))


def glove(word2index, index2word, sentences):
    print('GloVe')


def sentence2word(sentence):
    """
    Converts sentence to list of words. Gets rid of non alphanumeric characters
    :param sentence: Sentence we wish to split
    :return: list of strings
    """
    return list(filter(lambda word: word != "", [re.sub('[^A-Za-z0-9]+', '', word).lower() for word in sentence.replace("' ", "'").split(' ')]))


def doc2sentence(doc):
    """
    Converts document with carriage returns to list of strings.
    :param doc: Document we wish to split
    :return: list of strings
    """
    sentences = doc.split('\n')
    sentences = list(filter(lambda sentence: sentence not in("", " ", "\n"), sentences))
    return sentences
