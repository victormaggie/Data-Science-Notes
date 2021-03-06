# Here is the image preprocessing part for the calculation

import tensorflow as tf

# get the image vector
def decode_image(filename, image_type, resize_shape, channels=0):
    value = tf.read_file(filename)
    if image_type == 'png':
        decoded_image = tf.image.decode_png(value, channels=channels)
    elif image_type == 'jpeg':
        decoded_image = tf.image.decode_jpeg(value, channels)
    else:
        decoded_image = tf.image.decode_image(value, channels=channels)
    if resize_shape and image_type in ('png', 'jpeg'):
        decoded_image = tf.image.resize_images(decoded_image, resize_shape)
    return decoded_image
    
# get the data file
def get_dataset(image_paths, image_type, resize_shape, channels):
    filename_tensor = tf.constant(image_paths)
    dataset = tf.data.Dataset.from_tensor_slices(filename_tensor)
    def _map_fn(filename):
        return ref_decode_image(filename, image_type, resize_shape, channels=channels)
    # generate a mapping object
    return dataset.map(_map_fn)
    
# set up a iterator to extractor data from a pixel array dataset
def get_image_data(image_paths, image_type=None, resize_shape=None, channels=0):
    # define iterator
    dataset = get_dataset(image_paths, image_type, resize_shape, channels)
    iterator = dataset.make_one_shot_iterator()
    # pop the next one
    next_image = iterator.get_next()

    # execution data extraction in Tensorflow by using tf.Session
    # use tf.Session() to extract the data and put in the list
    image_data_list = []
    with tf.Session() as sess:
        for i in range(len(image_paths)):
            image_data = sess.run(next_image)
            image_data_list.append(image_data)   
    return image_data_list
    
# Processing the large scale image processing in Tensorflow 
# PIL module allows us to do more fine-grained image processing

import numpy as np
from PIL import Image, ImageFilter

# Load and resize an image using PIL, and return its pixel data
def pil_resize_image(image_path, resize_shape,
    image_mode='RGBA', image_filter=None):
    # CODE HERE
    im = Image.open(image_path)
    converted_im = im.convert(image_mode)
    resized_im = converted_im.resize(resize_shape, Image.LANCZOS)
    # change filter
    if image_filter:
        resized_im = resized_im.filter(image_filter)
    # get the resize
    im_data = resized_im.getdata()
    return np.asarray(im_data)

























