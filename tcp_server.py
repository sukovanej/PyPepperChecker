"""TCP Server module"""

import socket
import os
from PIL import Image
import numpy
import cv2


class TcpServer(object):
    """
    Tcp Server
    """
    TCP_IP = "0.0.0.0"
    TCP_PORT = 9090
    DIR = "./unknown"

    def __init__(self, network):
        self.network = network

    def run(self):
        """
        run TCP server
        """
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcp_socket.bind((self.TCP_IP, self.TCP_PORT))
        tcp_socket.listen(True)

        # while (True):
        connection, addr = tcp_socket.accept()
        print(" --- new connection")
        length = self._recvall(connection, 4)
        size = self._packet_length(length)

        print("size: {}".format(size))

        stringData = self._recvall(connection, int(size))
        data = numpy.fromstring(stringData, dtype='uint8')

        file = "./unknown/{}.jpg".format(len([name for name in os.listdir(self.DIR)
            if os.path.isfile(os.path.join(self.DIR, name))]))

        image = cv2.imdecode(data, 1)
        cv2.imwrite(file, image)

        tcp_socket.close()

    def _recvall(self, sock, count):
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
