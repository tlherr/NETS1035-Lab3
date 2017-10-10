"""
 Thomas Herr
 200325519

 Code modified from original author: Ian McWilliam
 Also @Ref: http://code.activestate.com/recipes/531824-chat-server-client-using-selectselect/
 Server that listens for client connections
"""

import socket
import signal
import select
import logging
import sys
import queue
from threading import _start_new_thread

from libcrypto import aesdecrypt
from libcrypto import aesencrypt

class Server(object):

    def __init__(self, port=8886, socket_backlog=5):

        self.AES_KEY = '00112233445566778899aabbccddeeff'
        self.clients = 0

        # Attempt to create socket
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as msg:
            print("Unable to create socket", msg)
            exit(1)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.setblocking(0)

        # Attempt to bind port
        try:
            self.server.bind(('0.0.0.0', port))
        except socket.error as msg:
            print("Unable to bind to specified port", msg)
            exit(1)

        self.server.listen(socket_backlog)
        logging.info(f"Listening on port ${port}")

        # Sockets from which we expect to read
        self.input_sockets = [ self.server ]
        # Sockets to which we expect to write
        self.output_sockets = []
        # Outgoing message queues
        self.message_queues = {}

        self.broadcast_sockets = []

        # Trap keyboard interrupts
        signal.signal(signal.SIGINT, self.sighandler)


    def encrypt(self, message):
        return aesencrypt(self.AES_KEY, message)

    def decrypt(self, message):
        return aesdecrypt(self.AES_KEY, message)

    def sighandler(self, signum, frame):
        logging.warning("Server Shutting Down")
        # Close Sockets
        for o in self.output_sockets:
            o.close()
        self.server.close()
        exit(0)

    def serve(self):
        # Main loop, calls select to block and wait for network activity
        while self.input_sockets:
            # Wait for at least one of the sockets to be ready for processing
            logging.info(f"Waiting for the next event")
            readable, writable, exceptional = select.select(self.input_sockets, self.output_sockets, self.input_sockets)

            # Select returns three lists: readable, writeable and exceptional. Readable lists have incoming data buffered
            # and available to red. Writeable lists  have free space in buffer and can be written to. Sockets in exceptional
            # have had an error occur

            # Handle inputs
            for s in readable:
                if s is self.server:
                    # A "readable" server socket is ready to accept a connection
                    connection, client_address = s.accept()
                    print(f"New Connection From: ${client_address}")
                    connection.setblocking(0)
                    self.input_sockets.append(connection)

                    self.broadcast_sockets.append(connection)

                    # Give the connection a queue for data we want to send
                    self.message_queues[connection] = queue.Queue()
                else:
                    data = s.recv(1024)
                    # This case represents a client that has sent data. Data is read then placed onto the queue so it
                    if data:
                        # A readable client socket has data
                        print(f"received ${self.decrypt(data)} from ${s.getpeername()}")

                        for client in self.broadcast_sockets:
                            if(client==s):
                                self.message_queues[s].put(self.encrypt("Acknowledged"))
                            else:
                                self.message_queues[client].put(data)
                            self.output_sockets.append(client)

                    # No data means client has disconnected and socket is ready to be closed
                    else:
                        # Interpret empty result as closed connection
                        print(f"Closing ${client_address}, after reading no data")
                        # Stop listening for input on the connection
                        if s in self.output_sockets:
                            self.output_sockets.remove(s)
                        self.input_sockets.remove(s)
                        s.close()

                        # Remove message queue
                        del self.message_queues[s]
            # Handle outputs
            for s in writable:
                try:
                    next_msg = self.message_queues[s].get_nowait()
                    print(f"Message in writable queue: ${self.decrypt(next_msg)}")
                except queue.Empty:
                    # No messages waiting so stop checking for writability.
                    print(f"Output queue for ${s.getpeername()}, is empty")
                    self.output_sockets.remove(s)
                else:
                    print(f"sending ${self.decrypt(next_msg)} to ${s.getpeername()}")
                    # Want to send the message out on all output sockets except the one we recieved message on
                    s.send(next_msg)

            # Handle exceptions
            for s in exceptional:
                logging.info(f"handling exceptional condition for ${s.getpeername()}")
                # Stop listening for input on the connection
                self.input_sockets.remove(s)
                if s in self.output_sockets:
                    self.output_sockets.remove(s)
                s.close()

                # Remove message queue
                del self.message_queues[s]

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

    print("Server Starting")
    Server().serve()