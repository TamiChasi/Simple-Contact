#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import logging
import datetime

logging.basicConfig(filename='example.log', level=logging.DEBUG)


def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Greetings from the cave! Now type your name and press enter!"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""

    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
    client.send(welcome)
    msg = "%s has joined the chat!" % name
    broadcast(msg)
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        if msg != "{quit}":
            broadcast(msg, name + ": ")
        else:
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            client.send("{quit}")
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            break


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(prefix + msg)
    logging.info(prefix + msg)


clients = {}
addresses = {}

HOST = '192.168.105.3'
PORT = 36000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    #     logging.debug('This message should go to the log file')
    logging.info(datetime.datetime.now())
    logging.info('server is running.')
    logging.info('Waiting for connection...')
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()


