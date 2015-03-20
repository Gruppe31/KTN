# -*- coding: utf-8 -*-
import socket
import json
import threading
import re

class Client:
    """
    This is the chat client class
    """

    def __init__(self, host, server_port):
        """
        This method is run when creating a new Client object
        """

        # Set up the socket connection to the server
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.run()

        # TODO: Finish init process with necessary code

    def process_json(self, data):
        index = 0
        while data.find('{', index) >= 0:
            start = data.find('{', index)
            end = data.find('}', start)
            index = end
            self.process_data(data[start:end+1])

    def process_data(self, data):
        decoded = json.loads(data)
        if decoded.get('response', '') == 'login':
            if decoded.get('error', '') != '':
                print decoded['error'], '(%s)'%decoded.get('username', '')
            else:
                self.logged_in = True
            if decoded.get('messages', '') != '':
                print decoded['messages'].encode('utf-8')
        if not self.logged_in:
            return
        if decoded.get('response', '') == 'logout':
            self.logged_in = False
        if decoded.get('respnse', '') == 'message':
            print decoded['message'].encode('utf-8')

    def send(self, data):
        self.connection.sendall(data)

    def login(self):
        self.send(self.parse({'request':'login', 'username':self.username}))

    def parse(self, data):
        return json.dumps(data)

    def run(self):
        self.__init__()
        print 'Welcome to this chatprogram!\nPlease specify server ip:port, or leave blank for the defaults ' + self.host + ':' + str(self.server_port)
        innInfo = raw_input('>')
        if innInfo:
            host = innInnfo.split(':')[0]
            port = int(innInfo.split(':')[1])
        self.connection.connect((self.host, self.server_port))
        self.logged_in = False
        self.commands = {'/logout':self.disconnect}
        while not self.logged_in:
            self.username = raw_input('Username: ')
            self.login()
            response = self.connection.recv(1024).strip()
            self.process_json(response)
        t = threading.Thread(target = self.take_input)
        t.setDaemon = True
        t.start()
        while self.logged_in:
            received_data = self.connection.recv(1024).strip()
            self.process_json(received_data)
        self.connection.close()

    def disconnect(self):
        # TODO: Handle disconnection
        self.send(self.parse({'request':'logout'}))



if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations is necessary
    """
    client = Client('localhost', 9998)
