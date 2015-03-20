# -*- coding: utf-8 -*-
import SocketServer
import datetime

import time
import json

class userHandler():

    def __init__(self):
        self.connections = []
        self.users =[]
        self.history = []


    def addUser(self, user):
        self.users.append(user)

    def hasUser(self, user):
        for i in self.users:
            if i == user:
                return True
        return False

    def removeUser(self, user):
        self.users.remove(user)

    def getUsers(self):
        return self.users

    def addConnection(self, handler):
        self.connections.append(handler)

    def getConnections(self):
        return self.connections

    def removeConnection(self, conn):
        self.connections.remove(conn)
    def addMessage(self, message):
        self.history.append(message)

    def getHistory(self):
        return self.history


class ClientHandler(SocketServer.BaseRequestHandler):

    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """

    def handle(self):
        handler = userHandler()
        user = ''
        """
        This method handles the connection between a client and the server.
        """
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request

        # Loop that listens for messages from the client
        while True:
            hasLoggedIn = False
            received_string = self.connection.recv(4096)
            if type(received_string) != str:
                received_string = self.connection.recv(4096)
                try:
                    jrec = json.loads(received_string)
                    body = jrec["content"].encode()
                    request = jrec["request"].encode()

                except ValueError:
                    print("Not JSON-Object, trying again.")
            else:
                jrec = json.loads(received_string)
                body = jrec["content"]
                request = jrec["request"]

            if request == 'login' and not hasLoggedIn:
                if handler.hasUser(body):
                    tid = time.time()
                    thisTime = datetime.datetime.fromtimestamp(tid).strftime('%H:%M:%S')
                    response = {"Tidsstempel": thisTime, "Avsender": "Server", "Svar": "Innlogging", "Innhold": "Dette brukernavnet er allerede i bruk, vennligst velg et annet."}
                    print type(response)
                    jsonresponse = json.dumps(response)
                    self.connection.send(json.dumps(jsonresponse))

                else:
                    handler.addConnection(self)

                    user = body
                    tid = time.time()
                    thisTime = datetime.datetime.fromtimestamp(tid).strftime('%H:%M:%S')
                    response = {"Tidsstempel": thisTime, "Avsender": "Server", "Svar": "Innlogging", "Innhold": "Innlogging suksessfull."}
                    jsonresponse = json.dumps(response)
                    self.connection.send(jsonresponse)
                    history = handler.getHistory()
                    response = {"Tidsstempel": thisTime, "Avsender": "Server", "Svar": "Historie", "Innhold": history}
                    jsonresponse = json.dumps(response)
                    self.connection.send(jsonresponse)
                    print(body+" logget inn.")
                    handler.addUser(str(body))
            elif request == 'logout':
                print handler.getUsers()
                print handler.getConnections()
                handler.removeUser(str(body))
                print(body+" logget ut.")
                handler.removeConnection(self)
                tid = time.time()
                thisTime = datetime.datetime.fromtimestamp(tid).strftime('%H:%M:%S')
                obj = {"Tidsstempel": thisTime, "Avsender": "Server", "Svar": "Utlogging", "Innhold": "Utlogging suksessfull"}
                self.connection.close()

            elif request == 'names':
                tid = time.time()
                thisTime = datetime.datetime.fromtimestamp(tid).strftime('%H:%M:%S')
                response = {"Tidsstempel": thisTime, "Avsender": "Server", "Svar": "Navn", "Innhold": userHandler.getUsers()}
                jsonresponse = json.dumps(response)
                self.connection.send(jsonresponse)
            elif request == 'history':
                    tid = time.time()
                    thisTime = datetime.datetime.fromtimestamp(tid).strftime('%H:%M:%S')
                    history = handler.getHistory()
                    response = {"Tidsstempel": thisTime, "Avsender": "Server", "Svar": "Historie", "Innhold": history}
                    jsonresponse = json.dumps(response)
                    self.connection.send(jsonresponse)
            elif request == 'msg':
                print("Fikk Melding: "+body)
                tid = time.time()
                thisTime = datetime.datetime.fromtimestamp(tid).strftime('%H:%M:%S')
                obj = {"Tidsstempel": thisTime, "Avsender": user, "Svar": "Melding", "Innhold": body}
                jsonresponse = json.dumps(obj)
                handler.addMessage(jsonresponse)
                print("Lagt til "+body+" til historien")
                threads = handler.getConnections()
                tid = time.time()
                thisTime = datetime.datetime.fromtimestamp(tid).strftime('%H:%M:%S')
                response = {"Tidsstempel": thisTime, "Avsender": user, "Svar": "Melding", "Innhold": body}
                jsonresponse = json.dumps(response)
                for i in threads:
                    if i == self:
                        continue
                    else:
                        i.connection.send(jsonresponse)
                    #obj = i.connection.recv(4096)

            #elif request == 'msg' and not hasLoggedIn:
                #print
                #tid = time.time()
                #thisTime = datetime.datetime.fromtimestamp(tid).strftime('%H:%M:%S')
                #response = {"Timestamp": thisTime, "Sender": "Server", "Response": "Error", "Content": "You have to be logged in in order to send messages,"}
                #jsonresponse = json.dumps(response)
                #self.connection.send(jsonresponse)

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

