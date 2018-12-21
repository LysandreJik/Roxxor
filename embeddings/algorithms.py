import re
from random import random
import numpy as np
from keras.preprocessing.sequence import skipgrams, make_sampling_table
import pickle
from negative_sampling_softmax import negative_sampling_softmax_model, SimilarityCallback


def negative_sampling(word2index, index2word, sentences, K=5, create_new=True, skipgram_file=None):
    if not create_new and skipgram_file is None:
        raise ValueError("'skipgram_file' must be specified if 'create_new' is set to False.")

    vocab_size = len(word2index)
    vector_dim = 300
    epochs = 1000000

    sentences = [[word2index[word] for word in sentence2word(sentence)] for sentence in sentences]
    print(sentences)

    validation_size = 16
    validation_window = 100
    validation_examples = np.random.choice(validation_window, validation_size, replace=False)

    if create_new:
        sampling_table = make_sampling_table(vocab_size)
        couples, labels = [], []

        print('Creating skipgrams for ', len(sentences), "sentences")
        for index, sentence in enumerate(sentences):
            if index % 100 == 0:
                print('\r' + str(int(index*100/len(sentences))) + '%', end='')
            couple, label = skipgrams(sentences[0], vocab_size, window_size=validation_window, sampling_table=sampling_table)
            couples.extend(couple)
            labels.extend(label)

        if skipgram_file:
            pickle_out = open('skipgrams/'+skipgram_file+'.pickle', 'wb')
            pickle.dump({'couples': couples, 'labels': labels}, pickle_out)
            pickle_out.close()
    else:
        pickle_in = open("skipgrams/"+skipgram_file+".pickle", "rb")
        dict = pickle.load(pickle_in)
        couples = dict['couples']
        labels = dict['labels']

    word_target, word_context = zip(*couples)
    word_target = np.array(word_target, dtype="int32")
    word_context = np.array(word_context, dtype="int32")

    print([(index2word[i[0]], index2word[i[1]]) for i in couples[:10]], labels[:10])
    print('Couples:', len(couples))
    print('Labels:', len(labels))

    model, validation_model = negative_sampling_softmax_model(vocab_size, vector_dim)

    simulation_callback = SimilarityCallback(vocab_size, validation_size, word2index, index2word, validation_examples, validation_model)

    arr_1 = np.zeros((1,))
    arr_2 = np.zeros((1,))
    arr_3 = np.zeros((1,))

    for iteration in range(epochs):
        idx = np.random.randint(0, len(labels) - 1)
        arr_1[0,] = word_target[idx]
        arr_2[0,] = word_context[idx]
        arr_3[0,] = labels[idx]
        loss = model.train_on_batch([arr_1, arr_2], arr_3)
        if iteration % 100 == 0:
            print("Iteration {}, loss={}".format(iteration, loss))
        if iteration % 10000 == 0:
            simulation_callback.run_sim()


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
