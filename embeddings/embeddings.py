import json
import re


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

                post_sentences = Embeddings.doc2sentence(document['post'])
                for sentence in post_sentences:
                    self.sentences.append(sentence)

                comments = document['comments']
                for comment in comments:
                    comment_sentences = Embeddings.doc2sentence(comment)
                    for sentence in comment_sentences:
                        self.sentences.append(sentence)

        print('Total number of sentences:', len(self.sentences))
        self.words = []

        for sentence in self.sentences:
            for word in Embeddings.sentence2word(sentence):
                self.words.append(word)

        ordered_word_list = sorted([e for e in set(self.words)])

        self.word2index = {e: i for e, i in enumerate(ordered_word_list)}
        self.index2word = {i: e for e, i in enumerate(ordered_word_list)}

        print('word2index and index2word successfully built.')


    @staticmethod
    def doc2sentence(doc):
        """
        Converts document with carriage returns to list of strings.
        :param doc: Document we wish to split
        :return: list of strings
        """
        sentences = doc.split('\n')
        sentences = list(filter(lambda sentence: sentence not in("", " ", "\n"), sentences))
        return sentences

    @staticmethod
    def sentence2word(sentence):
        """
        Converts sentence to list of words. Gets rid of non alphanumeric characters
        :param sentence: Sentence we wish to split
        :return: list of strings
        """
        return[re.sub('[^A-Za-z0-9]+', '', word) for word in sentence.replace("' ", "'").split(' ')]


embeddings = Embeddings(['1013.json', '1012.json', '1011.json'])