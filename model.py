
# Feed in batches of string tweets
# put them into a word to vec model
# plot the vectors in matplotlib
# this is mainly to explrore word to vec 
import logging
import gensim.models.word2vec as w2v
import multiprocessing
import sklearn.manifold
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Set up Logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# Pass in a list of words adn print 
class Model():

    # Hyperparamters
    features = 300
    min_word_count = 3 #?
    workers = multiprocessing.cpu_count() 
    context_size = 7
    downsampling = 1e-3
    seed = 1

    def __init__(self):
        self.vec = w2v.Word2Vec(
                                sg=1,
                                seed=self.seed,
                                workers=self.workers,
                                size=self.features,
                                min_count=self.min_word_count,
                                window=self.context_size,
                                sample=self.downsampling) 

    def words(self, word_list):
        self.words = word_list
        print (self.words)

    def train(self, word_list):
        self.vec.build_vocab(word_list)
        #print("Word2Vec vocabulary length:", len(self.vec.vocab))
        count = self.vec.corpus_count
        print ("Count: {}".format(count))
        epochs = 5000
        self.vec.train(word_list, total_examples=count, epochs=epochs)
    
    def plot(self):
        #my video - how to visualize a dataset easily
        tsne = sklearn.manifold.TSNE(n_components=2, random_state=0)
        all_word_vectors_matrix = self.vec.wv.vectors
        all_word_vectors_matrix_2d = tsne.fit_transform(all_word_vectors_matrix)
        points = pd.DataFrame(
            [
                (word, coords[0], coords[1])
                for word, coords in [
                    (word, all_word_vectors_matrix_2d[self.vec.wv.vocab[word].index])
                    for word in self.vec.wv.vocab
                ]
            ],
            columns=["word", "x", "y"]
        )
        print (points.head(10))
        sns.set_context("poster")
        #points.plot.scatter("x", "y", s=10, figsize=(20, 12))
        slice = points
        ax = slice.plot.scatter("x", "y", s=35, figsize=(10, 8))
        for i, point in slice.iterrows():
            ax.text(point.x + 0.005, point.y + 0.005, point.word, fontsize=11)

        plt.show()
        








