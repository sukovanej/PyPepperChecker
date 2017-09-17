"""
PyPepperChecker module
"""

from tcp_server import TcpServer
from network import Network

OUTPUT_SIZE = 3
INPUT_SIZE = 172 * 229 * 3

print("Building neural network...")
network = Network(INPUT_SIZE, OUTPUT_SIZE)

print "Processing images samples..."
network.process_images()

print "Training network..."
network.train()

print("Running TCP server...")
tcp_server = TcpServer(network)
tcp_server.run()
