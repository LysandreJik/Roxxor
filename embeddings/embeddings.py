import json
import re
import os
from algorithms import negative_sampling, doc2sentence, sentence2word
from collections import Counter
import time


class Embeddings:
    """
    Create naive word embeddings with the given method. The files passed as parameters will contain the post and
    comments that we wish to use for these embeddings.
    """
    def __init__(self, files, method='negative_sampling'):
        self.method = method
        self.files = files
        self.sentences = []

        print('Parsing files')
        for file in files:
            with open('../posts/' + file, encoding='utf-8') as f:
                document = json.load(f)

                post_sentences = doc2sentence(document['post'])
                for sentence in post_sentences:
                    self.sentences.append(sentence)

                comments = document['comments']
                for comment in comments:
                    comment_sentences = doc2sentence(comment)
                    for sentence in comment_sentences:
                        self.sentences.append(sentence)

        print('Total number of sentences:', len(self.sentences))
        self.words = []

        for sentence in self.sentences:
            for word in sentence2word(sentence):
                self.words.append(word)

        print('Ordering word list ...')
        # ordered_word_list = sorted(set([i for i in self.words if self.words.count(i) > 2]))

        print(Counter(self.words).most_common(10000))

        ordered_word_list = list(dict.fromkeys([item for items, c in Counter(self.words).most_common() for item in [items] * c]))
        print('Word list ordered !')
        print(ordered_word_list)

        self.word2index = {key: value for value, key in enumerate(ordered_word_list)}
        self.index2word = {key: value for value, key in self.word2index.items()}

        print('word2index and index2word successfully built. Total number of different words:', len(ordered_word_list))

        negative_sampling(self.word2index, self.index2word, self.sentences, 4)


embeddings = Embeddings(os.listdir("../posts"))
