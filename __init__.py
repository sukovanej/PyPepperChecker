import os
from PIL import Image
from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer

from data_functions import getInputVector, getOutputVector
from tcp_server import run

dataset_raw = list()

output_size = 3
input_size = 172 * 229 * 3

data_dic = ("chala", "penis", "seven")

print("Processing images samples...")

for filename in os.listdir("./data_smaller"):
    image = Image.open("./data_smaller/" + filename)

    pixels = list(image.getdata())

    if filename.startswith(data_dic[0]):
        dataset_raw.append([ 0, pixels ])
    elif filename.startswith(data_dic[1]):
        dataset_raw.append([ 1, pixels ])
    elif filename.startswith(data_dic[2]):
        dataset_raw.append([ 2, pixels ])


print("Building neural network...")

network = buildNetwork(input_size, 100, 100, 100, output_size, bias=True)
dataset = SupervisedDataSet(input_size, output_size);

print("Building dataset...")

for output, input in dataset_raw:
    dataset.addSample(getInputVector(input), getOutputVector(output, output_size))

print("Got {} samples!".format(len(dataset)))

print("Training network...")

trainer = BackpropTrainer(network, dataset)

for i in range(2):
    result = trainer.train()
    print("Trained error: {}".format(result))


print("Running TCP server...")
run()

# while(True):
#     filename = raw_input("Give me a filename:")
#     image = Image.open("./unknown/" + filename)
#     pixels = list(image.getdata())
#     result = network.activate(getInputVector(pixels))
#
#     print(result)