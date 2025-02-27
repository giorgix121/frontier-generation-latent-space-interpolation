'''
#Train a simple deep CNN on the SVHN small images dataset.

Model from below paper All-CNN-A
Springenberg, J., Dosovitskiy, A., Brox, T., and Riedmiller,
M. Striving for simplicity: The all convolutional net. In
ICLR Workshops, 2015
'''

from __future__ import print_function
import keras
from scipy.io import loadmat
from keras.models import Model
from keras.layers import Dropout, Activation, Input, Dense, Flatten
from keras.layers import Conv2D, GlobalAveragePooling2D
from keras.callbacks import LearningRateScheduler
import os
import time
import numpy as np
import tensorflow as tf

def rgb_to_grayscale(images):
    return np.dot(images[...,:3], [0.2989, 0.5870, 0.1140])

def Model1_svhn(input_tensor=None, train=False):
    img_rows, img_cols, img_chn = 32, 32, 1
    input_shape = (img_rows, img_cols, img_chn)

    if train:
        batch_size = 32
        num_classes = 10
        epochs = 350
        datasetLoc = './'

        train_data = loadmat(datasetLoc+'train_32x32.mat')
        x_train = np.array(train_data['X'])
        y_train = train_data['y']
        test_data = loadmat(datasetLoc+'test_32x32.mat')
        x_test = np.array(test_data['X'])
        y_test = test_data['y']

        x_train = np.moveaxis(x_train, -1, 0)
        x_test = np.moveaxis(x_test, -1, 0)

        # Convert RGB to grayscale
        x_train = rgb_to_grayscale(x_train)
        x_test = rgb_to_grayscale(x_test)

        # Add channel dimension
        x_train = np.expand_dims(x_train, axis=-1)
        x_test = np.expand_dims(x_test, axis=-1)

        # Normalize data.
        x_train = x_train.astype('float32') / 255
        x_test = x_test.astype('float32') / 255

        y_train[y_train == 10] = 0
        y_train = np.array(y_train)
        y_test[y_test == 10] = 0
        y_test = np.array(y_test)

        # Convert class vectors to binary class matrices.
        y_train = keras.utils.to_categorical(y_train, num_classes)
        y_test = keras.utils.to_categorical(y_test, num_classes)

    input_tensor = Input(shape=input_shape)

    # Model definition
    x = Conv2D(96, (5, 5), padding='same', input_shape=input_shape)(input_tensor)
    x = Activation('relu')(x)
    x = Conv2D(96, (3, 3), padding='same', strides=(2, 2))(x)
    x = Activation('relu')(x)
    x = Dropout(0.5)(x)
    x = Conv2D(192, (5, 5), padding='same')(x)
    x = Activation('relu')(x)
    x = Conv2D(192, (3, 3), padding='same', strides=(2, 2))(x)
    x = Activation('relu')(x)
    x = Dropout(0.5)(x)
    x = Conv2D(192, (3, 3), padding='same')(x)
    x = Activation('relu')(x)
    x = Conv2D(192, (1, 1), padding='valid')(x)
    x = Activation('relu')(x)
    x = Conv2D(10, (1, 1), padding='valid')(x)
    x = Activation('relu')(x)
    x = GlobalAveragePooling2D()(x)
    x = Activation('softmax')(x)

    model = Model(input_tensor, x)

    if train:
        # compiling
        sgd = keras.optimizers.SGD(learning_rate=0.01, decay=1e-6, momentum=0.9, nesterov=True)
        model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

        model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs,
                  validation_data=(x_test, y_test), verbose=2, shuffle=True)

        # save model
        model.save_weights('./Model1_svhn_gray.weights.h5')

        score = model.evaluate(x_test, y_test, verbose=0)
        print('\n')
        print('Overall Test score:', score[0])
        print('Overall Test accuracy:', score[1])
    else:
        # model.load_weights('svhn/models/Model1_svhn_gray.weights.h5')
        model.load_weights('/Users/gigimerabishvili/Desktop/frontier-generation-latent-space-interpolation/svhn/models/Model1_svhn_gray.h5')

    return model

if __name__ == '__main__':
    # Overall Test score: 0.42967066168785095
    # Overall Test accuracy: 0.9563614130020142
    # Check if GPU is available and set up for use
    physical_devices = tf.config.list_physical_devices('GPU')
    if len(physical_devices) > 0:
        print(f'{len(physical_devices)} GPU(s) available. Setting memory growth to True.')
        for device in physical_devices:
            tf.config.experimental.set_memory_growth(device, True)
    else:
        print('No GPU available, using CPU.')
    model = Model1_svhn(train=False)

    # Save the entire model to a new .h5 file
    # model.save('Model1_svhn_converted.h5')
