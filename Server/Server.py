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
        clientLoggedIn = False
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
                global connections
                if data in users:
                    tid = time.time()
                    timestamp = datetime.datetime.fromtimestamp(tid).strftime('%H:%M:%S')
                    res = {"timestamp":timestamp,"sender":"Server","response":"error","content":"Brukernavnet er tatt."}
                    package = json.dumps(res)
                    self.connection.send(package)
                else:
                    tid = time.time()
                    timestamp = datetime.datetime.fromtimestamp(tid).strftime('%H:%M:%S')
                    res = {"timestamp":timestamp,"sender":"Server","response":"history","content":history}
                    clientLoggedIn = True                    
                    package = json.dumps(res)
                    connections.append(self)
                    users.append(data)
                    self.username = data
                    self.connection.send(package)
                    
            elif request == "names" and clientLoggedIn:
                tid = time.time()
                timestamp = datetime.datetime.fromtimestamp(tid).strftime('%H:%M:%S')
                res = {"timestamp":timestamp,"sender":"Server","response":"info","content": ' '.join(users)}
                package = json.dumps(res)
                self.connection.send(package)
            
            elif request == "logout" and clientLoggedIn:
                users.remove(data)
                connections.remove(self)
            
            elif request == "history" and clientLoggedIn:
                tid = time.time()
                timestamp = datetime.datetime.fromtimestamp(tid).strftime('%H:%M:%S')
                res = {"timestamp":timestamp,"sender":"Server","response":"history".encode(),"content": history}
                package = json.dumps(res)
                self.connection.send(package)
            elif request == "help":
                #Serveren skal sende tilbake en hjelpemelding
                pass
            elif request == "msg" and clientLoggedIn:
                tid = time.time()
                timestamp = datetime.datetime.fromtimestamp(tid).strftime('%H:%M:%S')
                res = {"timestamp":timestamp,"sender": self.username,"response":"message".encode(),"content": data}
                package = json.dumps(res)
                history.append(package)
                print data + " lagt til i historien." 
                    
                for con in connections:
                    con.connection.send(package)
            else:
                timestamp = datetime.datetime.fromtimestamp(tid).strftime('%H:%M:%S')
                res = {"timestamp":timestamp,"sender": "Server","response":"error".encode(),"content": "Du har ikke tilgang"}
                package = json.dumps(res)


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
