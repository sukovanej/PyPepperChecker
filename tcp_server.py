import socket
import io
from PIL import Image

def run():
    """
    run TCP server
    :return:
    """
    TCP_IP = "0.0.0.0"
    TCP_PORT = 9090

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(True)

    conn, addr = s.accept()
    length = conn.recv(4)

    print("new connection")

    size = ord(length[0]) * 16777216 + ord(length[1]) * 65536 + ord(length[2]) * 256 + ord(length[3])

    print "size: {}".format(size)

    stringData = conn.recv(size)
    data = Image.open(io.BytesIO(stringData))

    file = "./unknown/{}.jpg".format(len([name for name in os.listdir(DIR)
        if os.path.isfile(os.path.join(DIR, name))]))
    data.save(file);

    s.close()
