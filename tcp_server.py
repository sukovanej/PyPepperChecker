"""TCP Server module"""

import socket
import os
from PIL import Image


class TcpServer(object):
    """
    Tcp Server
    """

    TCP_IP = "192.168.0.158"
    TCP_PORT = 9090
    BUFFER_SIZE = 100

    def __init__(self, network):
        self.network = network

    def run(self):
        """
        run TCP server
        """
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.bind((self.TCP_IP, self.TCP_PORT))
        tcp_socket.listen(True)

        while (True):
            print(" --- new connection")
            connection, addr = tcp_socket.accept()
            length = recvall(connection, 4)
            size = self._packet_length(length)

            print("size: {}".format(size))

            stringData = recvall(connection, int(size))
            data = numpy.fromstring(stringData, dtype='uint8')

            file = "./unknown/{}.jpg".format(len([name for name in os.listdir(DIR)
                                                  if os.path.isfile(os.path.join(DIR, name))]))
            data.save(file)

    def recvall(self, sock, count):
        """
        :param count:
        :return:
        """
        buf = b''
        while count:
            newbuf = sock.recv(count)
            if not newbuf: return None
            buf += newbuf
            count -= len(newbuf)
        return buf

    def _packet_length(self, length):
        return ord(length[0]) * 16777216 + ord(length[1]) * 65536 + ord(length[2]) * 256 + ord(length[3])
