from contextlib import contextmanager
import socket


@contextmanager
def incoming_tcp_connection(host, port):
    ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ls.bind((host, port))
    ls.listen(1)
    outconn, addr = ls.accept()
    try:
        yield outconn
    finally:
        outconn.close()


@contextmanager
def outgoing_tcp_connection(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    try:
        yield s
    finally:
        s.close()
