"""TCP Server module"""

import socket
import os
from PIL import Image
import numpy
import cv2
import shutil


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

        while (True):
            connection, addr = tcp_socket.accept()

            self.start = self._recvall(connection, 1)
            self.cmd = ord(self._recvall(connection, 1))
            length = self._recvall(connection, 4)
            self.size = self._string_to_int(length)
            self.string_data = self._recvall(connection, int(self.size))
            self.checksum = self._recvall(connection, 1)
            self.end = self._recvall(connection, 1)

            print(" > new command {}".format(self.cmd))

            result = ""
            if self.cmd == 0x01:
                result = self._command_send_image()
            elif self.cmd == 0x02:
                result = self._command_save_image()

            connection.send(result)

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

    def _string_to_int(self, length):
        return ord(length[0]) * 16777216 + ord(length[1]) * 65536 + ord(length[2]) * 256 + ord(length[3])


    def _command_send_image(self):
        """
        send image
        :param string_data:
        :return:
        """

        print("new image")
        data = numpy.fromstring(self.string_data, dtype='uint8')
        file = "./unknown/{}.jpg".format(len([name for name in os.listdir(self.DIR)
            if os.path.isfile(os.path.join(self.DIR, name))]))

        image = cv2.imdecode(data, 1)
        cv2.imwrite(file, image)

        result = ''.join([str(int(x * 100) & 0xFF) for x in self.network.activate(file)])
        return self._create_command(result, 0x01)

    def _command_save_image(self):
        """
        save image correct output
        :return:
        """
        event_id = self._string_to_int(self.string_data)
        index = self._string_to_int(self.string_data[4:])
        os.rename("{}.jpg".format(event_id), "{}_{}.jpg".format(index, event_id))

        return self._create_command("OK", 0x02)

    def _create_command(self, input, command):
        """
        create packet data
        :param input:
        :param command:
        :return:
        """
        input_len = len(input)

        result = ""
        result += chr(0x09)
        result += chr(command)
        result += chr(input_len & 0xFFFFFFFF)
        result += input
        result += str(self._checksum(result))
        result += chr(0x04)

        return result

    def _checksum(self, input):
        """
        compute checksum
        :param input:
        :return:
        """
        result = 0

        for char in input:
            result += ord(char)

        return result & 0xFF
