import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import tensorflow as tf
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

# from tensorflow.python.client import device_lib
# local_device_protos = device_lib.list_local_devices()

def init():
    print("TensorFlow Version: ", tf.__version__)
    physical_devices = tf.config.list_physical_devices('GPU')
    print("Available GPUs: ", len(physical_devices), " - ", tf.test.gpu_device_name())
    print("Built with CUDA: ", tf.test.is_built_with_cuda())
    print("Built with GPU support: ", tf.test.is_built_with_gpu_support())


init()

tokenizer = Tokenizer()

with open("docs\\word-list\\sentences.txt") as vocab:
    tokenizer.fit_on_texts(vocab.readlines())
    tokenizer.texts_to_sequences(vocab.readlines())


