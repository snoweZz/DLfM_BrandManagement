import numpy as np

# this file is not used in the current pipeline

def probabilty_to_classencoding(y_pred):
    """
    Output of softmax is probability distribution,
    But we need the one hot encoding vector based on the class of
    highest probabilty.
    This function converts output of sigmoid to output class one hot encoding form
    """
    y_class = np.array(y_pred)
    idx = np.argmax(y_class, axis=-1)
    y_class = np.zeros(y_class.shape)
    y_class[np.arange(y_class.shape[0]), idx] = 1
    return y_class


def binary_class_to_label(binary_class):
    """
    Return the class value based on the one hot encoding vector
    """
    return (np.argmax(binary_class, axis=1))