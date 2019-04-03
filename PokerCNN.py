# -*- coding: utf-8 -*-

from __future__ import print_function

import lasagne
 ''' SAMPLE CODE FOR THE POKER-CNN NEURAL NETWORK TAKEN FROM RESEARCH PAPER '''

NUM_FILTERS = 16 
NUM_HIDDEN_UNITS = 1024
FILTER_SIZE = (3,3)
LEARNING_RATE =  0.01 
MOMENTUM = 0.9
DROPOUT_PROB = 0.5
BATCH_SIZE = 100
BORDER_SHAPE = "valid" 
 
def build_model(input_width, input_height, output_dim,
                batch_size=BATCH_SIZE):

    input_layer = lasagne.layers.InputLayer(
        shape=(batch_size, 5, input_width, input_height),
        )

    convolutional_1 = lasagne.layers.Conv2DLayer(
        input_layer,
        num_filters=NUM_FILTERS,
        filter_size= FILTER_SIZE, 
        border_mode=BORDER_SHAPE, 
        nonlinearity=lasagne.nonlinearities.rectify,
        W=lasagne.init.GlorotUniform(),
        )

    convolutional_1_1 = lasagne.layers.Conv2DLayer(
        convolutional_1,
        num_filters=NUM_FILTERS, 
        filter_size=FILTER_SIZE, 
        border_mode=BORDER_SHAPE, 
        nonlinearity=lasagne.nonlinearities.rectify,
        W=lasagne.init.GlorotUniform(),
        )

    max_pool_1 = lasagne.layers.MaxPool2DLayer(convolutional_1_1, ds=(2, 2))

    convolutional_2 = lasagne.layers.Conv2DLayer(
        max_pool_1,
        num_filters=NUM_FILTERS*2, 
        filter_size=FILTER_SIZE,
        border_mode=BORDER_SHAPE, 
        nonlinearity=lasagne.nonlinearities.rectify,
        W=lasagne.init.GlorotUniform(),
        )

    convolutional_2_2 = lasagne.layers.Conv2DLayer(
        convolutional_2,
        num_filters=NUM_FILTERS*2,
        filter_size=FILTER_SIZE, 
        border_mode=BORDER_SHAPE,
        nonlinearity=lasagne.nonlinearities.rectify,
        W=lasagne.init.GlorotUniform(),
        )

    max_pool_2 = lasagne.layers.MaxPool2DLayer(convolutional_2_2, ds=(2, 2))

    dense_layer = lasagne.layers.DenseLayer(
        max_pool_2,
        num_units=NUM_HIDDEN_UNITS,
        nonlinearity=lasagne.nonlinearities.rectify,
        W=lasagne.init.GlorotUniform(),
        )

    dropout_layer = lasagne.layers.DropoutLayer(dense_layer, p=DROPOUT_PROB)

    output_layer = lasagne.layers.DenseLayer(
        dropout_layer, 
        num_units=output_dim,
        nonlinearity=lasagne.nonlinearities.rectify, 
        W=lasagne.init.GlorotUniform(),
        )
    return output_layer
#
# Single Card Representation
#
# [0 0 0 0 0 0 0 0 0 0 0 0 0
# 0 0 0 0 0 0 0 0 0 0 0 0 0
# 0 0 0 0 0 0 0 0 0 0 0 0 1
# 0 0 0 0 0 0 0 0 0 0 0 0 0]  ==== > Assuming h,c,d,s ===> Ks
# 
# Hand Representation 
# 2 x Single Card {Private Cards}
# 5 x Single Card {Board}
#   
# These Representations represent the input to input layer
# 
