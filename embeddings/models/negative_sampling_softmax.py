from keras import Model
from keras.layers import Input, Embedding, Reshape, merge, Dense
import numpy as np

def negative_sampling_softmax_model(vocab_size, vector_dim):
    """
    Not using the Sequencial layer framework, but the functional API. We are sharing a single embedding layer
    for two different tensors (the target and the context), as well as an aux. output to measure similarity.
    :param vocab_size:
    :param vector_dim:
    :return:
    """

    # We're supplying individual context and target words, therefore the input size is 1
    input_target = Input((1,))
    input_context = Input((1,))

    # vocab_size is the number of rows of our embedding layer. vector_dim is the amount of dimensions for the word
    # embedding. It will be the number of columns of our embedding layer. The input_length is the size of our inputs.
    # Giving the layer a name allows us to access its weights once it is trained. His weights are the embedding
    # matrix E, we will therefore need to know them.
    embedding = Embedding(vocab_size, vector_dim, input_length=1, name='embedding')

    target = embedding(input_target)
    target = Reshape((vector_dim, 1))(target)

    context = embedding(input_context)
    context = Reshape((vector_dim, 1))(context)

    # Calculate the cosine similarity between the target and context words.
    similarity = merge.Dot(0, normalize=True)([target, context])
    dot_product = merge.Dot(1)([target, context])
    dot_product = Reshape((1,))(dot_product)
    output = Dense(1, activation='sigmoid')(dot_product)

    model = Model(inputs=[input_target, input_context], outputs=output)
    model.compile(loss='binary_crossentropy', optimizer='rmsprop')

    # This model uses the same Embedding layer as the training one.The weights are the same.
    # We want to run this validation model as a way to have feedback on how the model learns, not train it.
    # We therefore don't need to compile it.
    validation_model = Model(inputs=[input_target, input_context], output=similarity)

    return model, validation_model


# We want to create a callback that will be used at every validation step. This will ensure our model trains correctly.
class SimilarityCallback:
    def __init__(self, vocab_size, valid_size, word2index, index2word, validation_examples, validation_model):
        self.vocab_size = vocab_size
        self.valid_size = valid_size
        self.word2index = word2index
        self.index2word = index2word
        self.validation_examples = validation_examples
        self.validation_model = validation_model

    def run_sim(self):
        for i in range(self.valid_size):
            valid_word = self.index2word[self.validation_examples[i]]
            top_k = 8
            sim = self.__get_sim(self.validation_examples[i])
            nearest = (-sim).argsort()[1:top_k + 1]
            log_str = 'Nearest to %s:' % valid_word

            for k in range(top_k):
                close_word = self.index2word[nearest[k]]
                log_str = '%s %s,' % (log_str, close_word)
            print(log_str)

    def __get_sim(self, valid_word_id):
        sim = np.zeros((self.vocab_size,))

        in_arr1 = np.zeros((1,))
        in_arr2 = np.zeros((1,))

        for i in range(self.vocab_size):
            in_arr1[0, ] = valid_word_id
            in_arr2[0, ] = i

            out = self.validation_model.predict_on_batch([in_arr1, in_arr2])
            sim[i] = out
        return sim
