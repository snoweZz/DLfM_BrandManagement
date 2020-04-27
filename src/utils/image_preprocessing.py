from PIL import Image
from io import BytesIO
from keras.preprocessing.image import img_to_array
import numpy as np
import requests

# specify the size of the image, must match the size the models expect
target_size = (300, 300)


# this function takes a list of image URLs as input and converts them into a numpy array
def preprocessing(results):
    predict_images_list = []
    for result in range(len(results)):
        # get the image based on the 'display_url'
        response = requests.get(results[result], stream=True)
        # convert it into a bytes object
        bytes = BytesIO(response.content)
        # convert it into an Image object
        image = Image.open(bytes)

        # resize the image if necessary
        if image.size != target_size:
            image = image.resize(target_size)

        # convert the image to a keras array and finally to a numpy array
        train_image = img_to_array(image)
        train_image = np.array(train_image)

        predict_images_list.append(train_image)

    # convert the images_list into one numpy array (used as X_test for the model)
    images_np = np.stack(predict_images_list, axis=0)
    return images_np

