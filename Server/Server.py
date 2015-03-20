# -*- coding: utf-8 -*-
import SocketServer
import json
import threading
import time
import re

allMessages = []
users = []
#Globale variabler som holder alle meldingene som blir sendt av alle clientene. 
#Må være global for å ha mulighet til å dele data mellom alle ClientHandler-trådene.
#Alt som legges til i allMessages vil bli vist til alle brukerne

class ClientHandler(SocketServer.BaseRequestHandler):
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """

    global allMessages
    global users

    def broadcast(self, data):
        allMessages.append(data)
    #sender data til alle klienter

    def handle(self):
        """
        This method handles the connection between a client and the server.
        """
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request
        self.logged_in = False

        #si ifra at en ny klient har koblet til serveren
        print 'Client connected @' + self.ip + ':' + str(self.port)

        #så man vet hvor mange av meldingene man har allerede har sendt
        self.sentdata = 0

        #få send_Updates til å fungere i en tråd
        t = threading.Thread(target = self.send_Updates)
        t.setDaemon = true
        t.start()

        # Loop that listens for messages from the client
        while True:
            received_string = self.connection.recv(4096)
            data = received_string.strip()
            # TODO: Add handling of received payload from client
            #sjekker om data eksisterer, recv kan returnere ved frakobling
            if data:
                self.broadcast(data)
                print data
            else:
                print('Client disconnected')
                break

    def processData(self, data):
        decoded = json.loads(data)
        if (decoded.get['request'] == 'login'):
            login(decoded.get('username', ''))
        if not logged_in:
            return
        if (decoded['request'] == 'logout'):
            logout()
        if (decoded['request'] == 'message'):
            newMessage(decoded('message'))

    def newMessage(self):
        if(self.user):
                sendToAll("[" + datetime.now().time() + "] <" + self.user + "> " + message)

    def login(self, username):
        if(not re.match(r'^[A-Za-z0-9_]+$', username)):
            send({'response': 'login', 'error': 'Invalid username!', 'username': username})
            return
        if not username in users: #true hvis ikke logget inn, false hvis allerede logget inn
            self.username = username
            users.append(username)                
            self.logged_in = True
            send({'response': 'login', 'username': username, 'messages': allMessages})
            self.broadcast('*** ' + self.username + ' has joined the chat.')
        else:
            send({'response': 'login', 'error': 'Name already taken', 'username': username})

    def logout(self):
        if(checkOut(self.username)):
            send({'respnse': 'logout', 'nick': self.username})
        else:
            send({'response': 'logout', 'error':'Not logged in!', 'nick': self.username})
        self.connection.close()

    def getUser(self, up, port):
        try:
            return "Nixo"
        except:
            print("User not found"):
            return "**Invalid User**"

    def send(self, data):
        self.request.sendall(json.dumps(data))

    def send_updates(self):
        while True:                
            if self.sentdata < len(allMessages):
                for i in range(self.sentdata, len(allMessages)):
                    self.connection.sendall(allMessages[i])
                    self.sentdata += 1
            time.sleep(0.2)

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