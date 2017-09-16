import socket
from PIL import Image

def run():
    """
    run TCP server
    :return:
    """
    TCP_IP = "192.168.0.158"
    TCP_PORT = 9090
    BUFFER_SIZE = 100

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(True)

    while (True):
        print(" --- new connection")
        conn, addr = s.accept()
        length = recvall(conn, 16)

        stringData = recvall(conn, int(length))
        data = Image.fromstring(stringData, dtype='uint8')

        file = "./unknown/{}.jpg".format(len([name for name in os.listdir(DIR)
                                              if os.path.isfile(os.path.join(DIR, name))]))
        data.save(file);
