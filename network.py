"""
Network module
"""
import os
from PIL import Image
from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from data_functions import get_input_vector, get_output_vector


class Network(object):
    """
    Network class
    """

    SAMPLES_DIR = "./data_smaller"

    def __init__(self, input_size, output_size):
        """
        Constructor
        """
        self.input_size = input_size
        self.output_size = output_size
        self.network = buildNetwork(
            input_size, 100, 100, 100, output_size, bias=True)
        self.data_dic = ("", "penis", "seven")
        self.dataset = list()

    def process_images(self):
        """
        Search for training set of images
            - load all sample images pixels
            - set supervised dataset
            - add all samples to the network
        """
        dataset_raw = list()

        for filename in os.listdir(self.SAMPLES_DIR):
            image = Image.open(self.SAMPLES_DIR + "/" + filename)

            pixels = list(image.getdata())
            dataset_raw.append([filename.split("_")[0], pixels])

        self.dataset = SupervisedDataSet(self.input_size, self.output_size)

        for output, input_vector in dataset_raw:
            self.dataset.addSample(get_input_vector(
                input_vector), get_output_vector(output, self.output_size))

    def train(self):
        """
        Train neural network using Backpropagation
        """
        trainer = BackpropTrainer(self.network, self.dataset)

        for i in range(2):
            result = trainer.train()
            print("Epoch {}, error = {}".format(i, result))
