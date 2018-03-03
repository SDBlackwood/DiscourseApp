import tensorflow as tf

from tensorflow.examples.tutorials.mnist import input_data
mnsit = input_data.read_data_sets('/tmp/data', one_hot=True)

# Set parameters
learning_rate = 0.01
training_iteration = 300
batch_size = 100
display_step = 10

#net work parameters 
n_input = 784
