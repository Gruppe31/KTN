# -*- coding: utf-8 -*-
import socket
from MessageReceiver import MessageReceiver
import json

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
        self.host = host
        self.server_port = server_port
        self.msgRec = MessageReceiver(self,self.connection)
        self.hasLoggedOn = False
        self.run()

    def run(self):
        # Initiate the connection to the server
        
        self.msgRec.start()
        
        while True:
            command = raw_input('')
            if command == "#logginn":
                print 'Skriv inn ditt onskede brukernavn'
                username = raw_input('')
                data = {"request":"login","content":username}
                try:
                    package = json.dumps(data)
                    self.connection.connect((self.host, self.server_port))
                    self.send_payload(package)
                    self.hasLoggedOn = True
                except UnicodeDecodeError:
                    print("Ikke bruk norske bokstaver.")
                    continue
                
            elif command == "#hjelp":#skal faa hjelpemelding fra server
                print "hjelpmelding"
                
            elif command == "#navn":
                #faa navn fra server
                data = {"request":"names","content":""}
                package = json.dumps(data)
                self.send_payload(package)
                
            elif command == "#loggut" and self.hasLoggedOn:
                data = {"request":"logout","content":username}
                package = json.dumps(data)
                self.send_payload(package)
                self.disconnect()
                self.hasLoggedOn = False
                print "Du er naa logget ut"
                
            elif command == "#historie" and self.hasLoggedOn:
                #faa historie fra serveren
                data = {"request":"history","content":""}
                package = json.dumps(data)
                self.send_payload(package)
                
            else:
                if self.hasLoggedOn:
                    data = {"request":"msg","content":command}
                    try:
                        package = json.dumps(data)
                        self.send_payload(package)
                    except UnicodeDecodeError:
                        print("Ikke bruk norske bokstaver.")
                        continue
                else:
                    print "Du maa vaere logget inn for aa gjore det"
                

    def disconnect(self):
        # TODO: Handle disconnection
        self.connection.close()

    def receive_message(self, message):
        # TODO: Handle incoming message
        jsonRec = json.loads(message)
        timestamp = jsonRec["timestamp"]
        sender = jsonRec["sender"]
        response = jsonRec["response"]
        content = jsonRec["content"]
        
        msg = "[" + response + " " + timestamp + " " + sender + "] " + content
        print msg
#        if response == "history":
#            for his in content:            
#                jsonRec = json.loads(his)
#                timestamp = jsonRec["timestamp"]
#                sender = jsonRec["sender"]
#                response = jsonRec["response"]
#                content = jsonRec["content"]
#                msg = "[" + timestamp + " " + sender + "] " + content
#                print msg
#        elif response == "message":
#            msg = "[" + timestamp + " " + sender + "] " + content
#            print msg
#        elif response == "info":
#            print content
#        elif response == "error":
#            print content
            
        
    def send_payload(self, data):
        # TODO: Handle sending of a payload
        self.connection.send(data)


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations is necessary
    """
    client = Client('localhost', 9998)
