import numpy as np


def give_ovr_class_label_output(y_pred):
    '''
    Stack 4 probabilities to get a numpy array
    '''
    yclass = np.hstack((y_pred[0], y_pred[1], y_pred[2], y_pred[3]))

    y_class = np.array(yclass)
    '''
    Get the index corresponding to the max value of column
    '''
    idx = np.argmax(y_class, axis=-1)
    y_class = np.zeros(y_class.shape)
    '''
    Convert the one hot position into class label
    '''
    y_class[np.arange(y_class.shape[0]), idx] = 1
    y_train_pred = np.argmax(y_class, axis=1)
    return y_train_pred