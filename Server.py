# -*- coding: utf-8 -*-
import SocketServer
import json
import datetime
import time

users = []
history = []
connections = []

def addUsers(user):
    global users
    users.append(user)

class ClientHandler(SocketServer.BaseRequestHandler):
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """

    def handle(self):
        """
        This method handles the connection between a client and the server.
        """
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request
        self.username = ""

        # Loop that listens for messages from the client
        while True:
            received_string = self.connection.recv(4096)
            if type(received_string) != str:
                received_string = self.connection.recv(4096)
                try:
                    jrec = json.loads(received_string)
                    data = jrec["content"].encode()
                    request = jrec["request"].encode()

                except ValueError:
                    print("Not JSON-Object, trying again.")
            else:
                jrec = json.loads(received_string)
                data = jrec["content"]
                request = jrec["request"]
                
            if request == "login":
                #login
                global users
                global connections
                if data in users:
                    tid = time.time()
                    timestamp = datetime.datetime.fromtimestamp(tid).strftime('%H:%M:%S')
                    res = {"timestamp":timestamp,"sender":"Server","response":"login","content":"Brukernavnet er tatt."}
                    package = json.dumps(res)
                    self.connection.send(package)
                else:
                    tid = time.time()
                    timestamp = datetime.datetime.fromtimestamp(tid).strftime('%H:%M:%S')
                    res = {"timestamp":timestamp,"sender":"Server","response":"login","content":"Suksess."}
                    package = json.dumps(res)
                    connections.append(self)
                    users.append(data)
                    self.username = data
                    self.connection.send(package)
                    
                
            if request == "names":
                #names
                global users
                tid = time.time()
                timestamp = datetime.datetime.fromtimestamp(tid).strftime('%H:%M:%S')
                res = {"timestamp":timestamp,"sender":"Server","response":"names","content": ' '.join(users)}
                package = json.dumps(res)
                self.connection.send(package)
            if request == "logout":
                #logout
                global users
                global connections
                users.remove(data)
                connections.remove(self)
            if request == "history":
                #history
                global history
                tid = time.time()
                timestamp = datetime.datetime.fromtimestamp(tid).strftime('%H:%M:%S')
                res = {"timestamp":timestamp,"sender":"Server","response":"history","content": history}
                package = json.dumps(res)
                self.connection.send(package)
                
            if request == "msg":
                global history
                global connection
                global users
                tid = time.time()
                timestamp = datetime.datetime.fromtimestamp(tid).strftime('%H:%M:%S')
                for con in connections:
                    
                    res = {"timestamp":timestamp,"sender": self.username,"response":"msg","content": data}
                    history.append(data)
                    package = json.dumps(res)
                    con.connection.send(package)
                    
            
            # TODO: Add handling of received payload from client


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.

    No alterations is necessary
    """
    allow_reuse_address = True

if __name__ == "__main__":
    """
    This is the main method and is executed when you type "python Server.py"
    in your terminal.

    No alterations is necessary
    """
    HOST, PORT = 'localhost', 9998
    print 'Server running...'

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()
