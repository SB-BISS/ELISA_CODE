import os
from keras.models import Sequential, Model
from keras.layers.normalization import BatchNormalization
from keras.layers.convolutional import Conv2D, Conv1D
from keras.layers.convolutional import Convolution2D
from keras.layers.convolutional import MaxPooling2D, MaxPooling1D
from keras.layers.core import Activation
from keras.layers.core import Flatten
from keras.layers.core import Dropout
from keras.layers.core import Dense, Layer
from keras.layers import concatenate, Input, dot, Lambda, Maximum
from keras import backend as K
import tensorflow as tf
import numpy as np
import imutils
from transformer import SpatialTransformer

# Small 1D vgg
# No recurrency for the moment
# Treating this as if it was an image even

def small_vgg(width, height, depth, classes, params=[32,64,128,1024],stride=5, categorical = "binary"):
    # initialize the model along with the input shape to be
    # "channels last" and the channels dimension itself
    model = Sequential()
    inputShape = (height, width, depth)
    chanDim = -1

    if K.image_data_format() == "channels_first":
        inputShape = (depth, height, width)
        chanDim = 1

    model.add(Conv2D(params[0], (stride, stride), padding="same",
                     input_shape=inputShape))
    model.add(Activation("relu"))
    model.add(BatchNormalization(axis=chanDim))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(params[1], (stride, stride), padding="same"))
    model.add(Activation("relu"))
    model.add(BatchNormalization(axis=chanDim))
    model.add(Conv2D(params[1], (stride, stride), padding="same"))
    model.add(Activation("relu"))
    model.add(BatchNormalization(axis=chanDim))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(params[2], (stride, stride), padding="same"))
    model.add(Activation("relu"))
    model.add(BatchNormalization(axis=chanDim))
    model.add(Conv2D(params[2], (stride, stride), padding="same"))
    model.add(Activation("relu"))
    model.add(BatchNormalization(axis=chanDim))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(params[3]))
    model.add(Activation("relu"))
    model.add(BatchNormalization())
    model.add(Dropout(0.5))

    # softmax classifier
    model.add(Dense(classes))
    if categorical == "categorical":
        model.add(Activation("softmax"))
    elif categorical=="binary":
        model.add(Activation("sigmoid"))
    else:
        model.add(Activation("relu"))

    # return the constructed network architecture
    return model


def small_vgg_fft(width, height, depth, classes, params=[32,64,128,1024], stride=5):
    # initialize the model along with the input shape to be
    # "channels last" and the channels dimension itself
    model = Sequential()
    inputShape = (height, width, depth)
    chanDim = -1

    if K.image_data_format() == "channels_first":
        inputShape = (depth, height, width)
        chanDim = 1

    model.add(Conv2D(params[0], (stride, stride), padding="same",
                     input_shape=inputShape))
    model.add(FFT_CONV())
    model.add(Activation("relu"))
    model.add(BatchNormalization(axis=chanDim))
    model.add(MaxPooling2D(pool_size=(3, 3)))
    model.add(Dropout(0.25))

    model.add(Conv2D(params[1], (stride, stride), padding="same"))
    model.add(FFT_CONV())

    model.add(Activation("relu"))
    model.add(BatchNormalization(axis=chanDim))
    model.add(Conv2D(params[1], (stride, stride), padding="same"))
    model.add(FFT_CONV())

    model.add(Activation("relu"))
    model.add(BatchNormalization(axis=chanDim))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(params[2], (stride, stride), padding="same"))
    model.add(FFT_CONV())

    model.add(Activation("relu"))
    model.add(BatchNormalization(axis=chanDim))
    model.add(Conv2D(params[2], (3, 3), padding="same"))
    model.add(FFT_CONV())

    model.add(Activation("relu"))
    model.add(BatchNormalization(axis=chanDim))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(params[3]))
    model.add(Activation("relu"))
    model.add(BatchNormalization())
    model.add(Dropout(0.5))

    # softmax classifier
    model.add(Dense(classes))
    model.add(Activation("sigmoid"))

    # return the constructed network architecture
    return model



def spatial_multi(width, height, depth,downsampling, classes, params=[32,64,128,1024], stride=5, categorical=True):
    
    
    model = Sequential()
    inputShape = (height, width, depth)
    chanDim = -1

    if K.image_data_format() == "channels_first":
        inputShape = (depth, height, width)
        chanDim = 1

    b = np.zeros((2, 3), dtype='float32')
    b[0, 0] = 1
    b[1, 1] = 1
    W = np.zeros((50, 6), dtype='float32')
    weights = [W, b.flatten()]
    
    locnet = Sequential()
    locnet.add(Conv2D(params[0], (stride, stride), padding="same",
                     input_shape=inputShape))
    
    locnet.add(MaxPooling2D(pool_size=(2,2)))
    locnet.add(Conv2D(params[0], (5, 5)))
    locnet.add(MaxPooling2D(pool_size=(2,2)))
    locnet.add(Conv2D(params[0], (5, 5)))
    locnet.add(Flatten())
    locnet.add(Dense(50))
    locnet.add(Activation('relu'))
    #locnet.add(Dense(2,weights=weights, activation="relu")) # angle
    
    locnet.add(Dense(6,weights=weights)) # angle
    
    
    
    chanDim = -1

    if K.image_data_format() == "channels_first":
        inputShape = (depth, height, width)
        chanDim = 1
    
    model = Sequential()
    #
    #model.add(FFT_IN(input_shape=(*shape,3),name='FFT_IN'))
    #model.add(Rot2D(name="ROT",input_shape=(*shape,3)))
    
    mysp = SpatialTransformer(localization_net=locnet, name="LocNet",
                              output_size=(int(inputShape[0]/downsampling),int(inputShape[1]/downsampling),inputShape[2]),
                              input_shape=inputShape)
    model.add(mysp)
    
    model.add(Conv2D(params[0], (stride, stride), padding="same",
                     input_shape=inputShape))
    model.add(Activation("relu"))
    model.add(BatchNormalization(axis=chanDim))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(params[1], (stride, stride), padding="same"))
    model.add(Activation("relu"))
    model.add(BatchNormalization(axis=chanDim))
    model.add(Conv2D(params[1], (stride, stride), padding="same"))
    model.add(Activation("relu"))
    model.add(BatchNormalization(axis=chanDim))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(params[2], (stride, stride), padding="same"))
    model.add(Activation("relu"))
    model.add(BatchNormalization(axis=chanDim))
    model.add(Conv2D(params[2], (stride, stride), padding="same"))
    model.add(Activation("relu"))
    model.add(BatchNormalization(axis=chanDim))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(params[3]))
    model.add(Activation("relu"))
    model.add(BatchNormalization())
    model.add(Dropout(0.5))

    # softmax classifier
    model.add(Dense(classes))
    if categorical == True:
        model.add(Activation("softmax"))
    else:
        model.add(Activation("sigmoid"))

    # return the constructed network architecture
    return model





def fft_vgg_rot(classes, shape=(75,75)):
    
    b = np.zeros((2, 3), dtype='float32')
    b[0, 0] = 1
    b[1, 1] = 1
    W = np.zeros((50, 6), dtype='float32')
    weights = [W, b.flatten()]
    
    locnet = Sequential()
    locnet.add(MaxPooling2D(pool_size=(2,2), input_shape=(*shape,3)))
    locnet.add(Conv2D(20, (5, 5)))
    locnet.add(MaxPooling2D(pool_size=(2,2)))
    locnet.add(Conv2D(20, (5, 5)))
    locnet.add(Flatten())
    locnet.add(Dense(50))
    locnet.add(Activation('relu'))
    #locnet.add(Dense(2,weights=weights, activation="relu")) # angle
    
    locnet.add(Dense(6,weights=weights)) # angle
    
    
    
    chanDim = -1

    if K.image_data_format() == "channels_first":
        inputShape = (depth, height, width)
        chanDim = 1
    
    model = Sequential()
    #
    #model.add(FFT_IN(input_shape=(*shape,3),name='FFT_IN'))
    #model.add(Rot2D(name="ROT",input_shape=(*shape,3)))
    
    model.add(SpatialTransformer(localization_net=locnet, name="LocNet",
                             output_size=shape, input_shape=(*shape,3)))
    
    model.add(FFT_IN(name='FFT_IN'))
    
    model.add(Convolution2D_8(filters=32, kernel_size=(3, 3), padding="same", name="Conv8"))
    model.add(FFT_IN(name='FFT_IN2'))

    model.add(Activation("relu"))
    model.add(BatchNormalization(axis=chanDim))
    model.add(MaxPooling2D(pool_size=(3, 3)))
    model.add(Dropout(0.25))

    model.add(Conv2D(64, (3, 3), padding="same"))
    #model.add(Rot2D(name="ROT2"))
    
    model.add(FFT_IN(name='FFT_IN3'))

    model.add(Activation("relu"))
    model.add(BatchNormalization(axis=chanDim))
    model.add(Conv2D(64, (3, 3), padding="same"))
    model.add(FFT_IN(name='FFT_IN4'))

    model.add(Activation("relu"))
    model.add(BatchNormalization(axis=chanDim))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(128, (3, 3), padding="same"))
    model.add(FFT_IN(name='FFT_IN5'))

    model.add(Activation("relu"))
    model.add(BatchNormalization(axis=chanDim))
    model.add(Conv2D(128, (3, 3), padding="same"))
    model.add(FFT_IN(name='FFT_IN6'))
    
    model.add(Activation("relu"))
    model.add(BatchNormalization(axis=chanDim))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(1024))
    model.add(Activation("relu"))
    model.add(BatchNormalization())
    model.add(Dropout(0.5))

    # softmax classifier
    model.add(Dense(classes))
    model.add(Activation("softmax"))

    # return the constructed network architecture
    return model










class FFT_CONV(Layer):

    #this is a 2D FFT frequency blurring layer
    #it works by cutting frequencies
    #that may not be interesting for the classification.

    def __init__(self, **kwargs):
        super(FFT_CONV, self).__init__(**kwargs)

    def build(self, input_shape):
        # Create a trainable weight variable for this layer.
        self.kernel = self.add_weight(name='kernel',
                                      shape=(1,) + input_shape[1:],
                                      initializer='he_normal',
                                      trainable=True
                                      )
        super(FFT_CONV, self).build(input_shape)  # Be sure to call this somewhere!

    def call(self, x):
        fft = tf.fft2d(tf.cast(x, dtype=tf.complex64))
        real = tf.real(fft) * tf.sigmoid(self.kernel)  # because you want to cut frequencies, not enhance them
        imag = tf.imag(fft)
        full = tf.complex(real, imag)
        full = abs(tf.ifft2d(full))
        self.kernel = tf.nn.l2_normalize(self.kernel)
        return full

    def compute_output_shape(self, input_shape):
        return input_shape
