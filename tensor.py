from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import math
import os
import sys
import argparse
import random
from tempfile import gettempdir
import zipfile
import traceback
import sys
import pprint as p
import matplotlib.pyplot as plt
import numpy as np
from six.moves import urllib
from six.moves import xrange  # pylint: disable=redefined-builtin
import tensorflow as tf
from sklearn.manifold import TSNE

from tensorflow.contrib.tensorboard.plugins import projector


class Tensor():
    '''
    A Wrapper class for the Tenflow operations
    '''

    data_index = 0
        # Step 2: Build the dictionary and replace rare words with UNK token.
    vocabulary_size = 1000
    
    FLAGS = object
    init = object
    num_steps = 0


    def __init__(self,num_steps):
        # Give a folder path as an argument with '--log_dir' to save
        # TensorBoard summaries. Default is a log folder in current directory.
        current_path = os.path.dirname(os.path.realpath(sys.argv[0]))
        self.num_steps = num_steps
        parser = argparse.ArgumentParser()
        parser.add_argument(
                                '--log_dir',
                                type=str,
                                default=os.path.join(current_path, 'log'),
                                help='The log directory for TensorBoard summaries.')
        self.FLAGS, unparsed = parser.parse_known_args()

        # Create the directory for TensorBoard variables if there is not.
        if not os.path.exists(self.FLAGS.log_dir):
            os.makedirs(self.FLAGS.log_dir)
            
  
    # Pass in a list of words in an array and the number of words are vocalb has
    def build_dataset(self, words):
        """Process raw inputs into a dataset."""
        count = [['UNK', -1]] 
        # Basically add all the top used words from the word array 
        count.extend(collections.Counter(words).most_common(self.vocabulary_size - 1))
        dictionary = dict()
        print (count)

        for word, _ in count:
            # For each str, make an entry into the dictionary and asign it a number
            # e.g ['word'] : 1
            dictionary[word] = len(dictionary)

        data = list()
        unk_count = 0

        for word in words:
            index = dictionary.get(word, 0)
            if index == 0:  # dictionary['UNK']
                unk_count += 1
                print (unk_count)
            data.append(index)
            
        count[0][1] = unk_count
        print (dictionary.values())
        print (dictionary.keys())
        reversed_dictionary = dict(zip(dictionary.values(), dictionary.keys()))
        return data, count, dictionary, reversed_dictionary

    def generate_batch(self, data, data_len, batch_size, num_skips, skip_window): 
        batch = np.ndarray(shape=(batch_size), dtype=np.int32)
        labels = np.ndarray(shape=(batch_size, 1), dtype=np.int32)
        span = 2 * skip_window + 1  # [ skip_window target skip_window ]
        buffer = collections.deque(maxlen=span)
        if self.data_index + span > data_len:
            self.data_index = 0
        buffer.extend(data[self.data_index:self.data_index + span])
        self.data_index += span
        for i in range(batch_size // num_skips):
            context_words = [w for w in range(span) if w != skip_window]
            words_to_use = random.sample(context_words, num_skips)
            for j, context_word in enumerate(words_to_use):
                batch[i * num_skips + j] = buffer[skip_window]
                labels[i * num_skips + j, 0] = buffer[context_word]
                if self.data_index == len(data):
                    buffer.extend(data[0:span])
                    self.data_index = span
                else:
                    buffer.append(data[self.data_index])
                    self.data_index += 1
        # Backtrack a little bit to avoid skipping words in the end of a batch
        self.data_index = (self.data_index + data_len - span) % len(data)
        return batch, labels
    


    def model(self, bag):
        # Build dataset
        data, count, dictionary, reverse_dictionary = self.build_dataset(bag)
        data_len = len(reverse_dictionary)-1
        print('Most common words (+UNK)', count[:5])
        print('Sample data', data[:10], [reverse_dictionary[i] for i in data[:10]])

        # Generate Batches
        batch, labels = self.generate_batch(data, data_len, batch_size=8, num_skips=2, skip_window=1)
        for i in range(8):
            print(batch[i], reverse_dictionary[batch[i]], '->', labels[i, 0],
                reverse_dictionary[labels[i, 0]])

        # Step 4: Build and train a skip-gram model.
        batch_size = 128
        embedding_size = 128  # Dimension of the embedding vector.
        skip_window = 1  # How many words to consider left and right.
        num_skips = 2  # How many times to reuse an input to generate a label.
        num_sampled = 64  # Number of negative examples to sample.

        # We pick a random validation set to sample nearest neighbors. Here we limit the
        # validation samples to the words that have a low numeric ID, which by
        # construction are also the most frequent. These 3 variables are used only for
        # displaying model accuracy, they don't affect calculation.
        valid_size = 16  # Random set of words to evaluate similarity on.
        valid_window = 100  # Only pick dev samples in the head of the distribution.
        valid_examples = np.random.choice(valid_window, valid_size, replace=False)


        graph = tf.Graph()
        with graph.as_default():

            # Input data.
            with tf.name_scope('inputs'):
                train_inputs = tf.placeholder(tf.int32, shape=[batch_size])
                train_labels = tf.placeholder(tf.int32, shape=[batch_size, 1])
                valid_dataset = tf.constant(valid_examples, dtype=tf.int32)

            # Ops and variables pinned to the CPU because of missing GPU implementation
            with tf.device('/cpu:0'):
                # Look up embeddings for inputs.
                with tf.name_scope('embeddings'):
                    embeddings = tf.Variable(
                        tf.random_uniform([data_len, embedding_size], -1.0, 1.0))
                    embed = tf.nn.embedding_lookup(embeddings, train_inputs)

                # Construct the variables for the NCE loss
                with tf.name_scope('weights'):
                    nce_weights = tf.Variable(
                        tf.truncated_normal(
                            [data_len, embedding_size],
                            stddev=1.0 / math.sqrt(embedding_size)))
                with tf.name_scope('biases'):
                    nce_biases = tf.Variable(tf.zeros([data_len]))

            # Compute the average NCE loss for the batch.
            # tf.nce_loss automatically draws a new sample of the negative labels each
            # time we evaluate the loss.
            # Explanation of the meaning of NCE loss:
            # http://mccormickml.com/2016/04/19/word2vec-tutorial-the-skip-gram-model/
            with tf.name_scope('loss'):
                loss = tf.reduce_mean(
                    tf.nn.nce_loss(
                        weights=nce_weights,
                        biases=nce_biases,
                        labels=train_labels,
                        inputs=embed,
                        num_sampled=num_sampled,
                        num_classes=data_len))

            # Add the loss value as a scalar to summary.
            tf.summary.scalar('loss', loss)

            # Construct the SGD optimizer using a learning rate of 1.0.
            with tf.name_scope('optimizer'):
                optimizer = tf.train.GradientDescentOptimizer(1.0).minimize(loss)

            # Compute the cosine similarity between minibatch examples and all embeddings.
            norm = tf.sqrt(tf.reduce_sum(tf.square(embeddings), 1, keepdims=True))
            normalized_embeddings = embeddings / norm
            valid_embeddings = tf.nn.embedding_lookup(normalized_embeddings,
                                                        valid_dataset)
            similarity = tf.matmul(
                valid_embeddings, normalized_embeddings, transpose_b=True)

            # Merge all summaries.
            merged = tf.summary.merge_all()

            # Add variable initializer.
            init = tf.global_variables_initializer()

            # Create a saver.
            saver = tf.train.Saver()

        # Step 5: Begin training.
        


        with tf.Session(graph=graph) as session:
            # Open a writer to write summaries.
            writer = tf.summary.FileWriter(self.FLAGS.log_dir, session.graph)

            # We must initialize all variables before we use them.
            init.run()
            print('Initialized')

            average_loss = 0
            for step in xrange(self.num_steps):
                batch_inputs, batch_labels = self.generate_batch(data, data_len,batch_size, num_skips, skip_window)
                feed_dict = {train_inputs: batch_inputs, train_labels: batch_labels}

                # Define metadata variable.
                run_metadata = tf.RunMetadata()

                # We perform one update step by evaluating the optimizer op (including it
                # in the list of returned values for session.run()
                # Also, evaluate the merged op to get all summaries from the returned "summary" variable.
                # Feed metadata variable to session for visualizing the graph in TensorBoard.
                _, summary, loss_val = session.run(
                    [optimizer, merged, loss],
                    feed_dict=feed_dict,
                    run_metadata=run_metadata)
                average_loss += loss_val

                # Add returned summaries to writer in each step.
                writer.add_summary(summary, step)
                # Add metadata to visualize the graph for the last run.
                if step == (self.num_steps - 1):
                    writer.add_run_metadata(run_metadata, 'step%d' % step)

                if step % 2000 == 0:
                    if step > 0:
                        average_loss /= 2000
                    # The average loss is an estimate of the loss over the last 2000 batches.
                    print('Average loss at step ', step, ': ', average_loss)
                    average_loss = 0

                # Note that this is expensive (~20% slowdown if computed every 500 steps)
                #if step % 1000 == 0:
                #    sim = similarity.eval()
                #for i in xrange(valid_size):
                #    valid_word = reverse_dictionary[valid_examples[i]]
                #    top_k = 8  # number of nearest neighbors
                #    nearest = (-sim[i, :]).argsort()[1:top_k + 1]
                #    log_str = 'Nearest to %s:' % valid_word
                #    for k in xrange(top_k): 
                #        close_word = reverse_dictionary[nearest[k]]         
                #        close_word = reverse_dictionary[nearest[k]]         
                #        log_str = '%s %s,' % (log_str, close_word)
                #    print(log_str)
            final_embeddings = normalized_embeddings.eval()

            # Write corresponding labels for the embeddings.
            with open(self.FLAGS.log_dir + '/metadata.tsv', 'w') as f:
                for i in xrange(len(reverse_dictionary)-1):
                    f.write(reverse_dictionary[i] + '\n')

            # Save the model for checkpoints.
            saver.save(session, os.path.join(self.FLAGS.log_dir, 'model.ckpt'))

            # Create a configuration for visualizing embeddings with the labels in TensorBoard.
            config = projector.ProjectorConfig()
            embedding_conf = config.embeddings.add()
            embedding_conf.tensor_name = embeddings.name
            embedding_conf.metadata_path = os.path.join(self.FLAGS.log_dir, 'metadata.tsv')
            projector.visualize_embeddings(writer, config)

            

        writer.close()
# Step 6: Visualize the embeddings.

        def plot_with_labels(low_dim_embs, labels, filename):
            assert low_dim_embs.shape[0] >= len(labels), 'More labels than embeddings'
            plt.figure(figsize=(18, 18))  # in inches
            for i, label in enumerate(labels):
                x, y = low_dim_embs[i, :]
                plt.scatter(x, y)
                plt.annotate(
                    label,
                    xy=(x, y),
                    xytext=(5, 2),
                    textcoords='offset points',
                    ha='right',
                    va='bottom')#

            plt.savefig(filename)


        # Dimensionality Reduction
        tsne = TSNE(
        perplexity=30, n_components=2, init='pca', n_iter=5000, method='exact')
        plot_only = 100
        low_dim_embs = tsne.fit_transform(final_embeddings[:plot_only, :])
        labels = [reverse_dictionary[i] for i in xrange(plot_only)]
        plot_with_labels(low_dim_embs, labels, os.path.join(gettempdir(), 'tsne.png'))

    def run(self, bag):
        self.model(bag)
        plt.show()
 

    
