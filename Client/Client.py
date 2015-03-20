# -*- coding: utf-8 -*-
import socket
import json
from MessageReceiver import MessageReceiver


class Client:
    """
    This is the chat client class
    """

    def __init__(self, host, server_port):
        self.hasloggedOn = False
        self.host = host
        self.server_port = server_port
        """
        This method is run when creating a new Client object
        """

        # Set up the socket connection to the server
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.msg = MessageReceiver(self, self.connection)

        self.run()

    def run(self):
        self.msg.start()
        # Initiate the connection to the server
        self.connection.connect((self.host, self.server_port))
        loggedOn = False
        print("Velkommen til denne chatten. Skriv inn -help hvis du trenger hjelp.")

        while True:

            income = raw_input()
            #income = unicode(rawincome, "utf-8")
            if income == '-help':
                helpCmd = ['Følgende kommandoer er nyttige:'
                '\n -login: skriv inn "login" og trykk enter, så en linje med ønsket brukernavn.'
                '\n -names: skriv inn bare dette for å se en liste over alle brukernavn som er opptatt i chatten.'
                '\n -logout: skriv bare dette for å logge av serveren.']
                for i in helpCmd:
                    print i
            elif income == '-login':
                print("Skriv inn ditt ønskede brukernavn og du vil bli logget på serveren så lenge brukernavnet ikker er tatt fra før.")

                income = raw_input()
                #income = unicode(rawincome, "utf-8")
                obj = {"request": "login", "content": income}
                try:
                    jsonobj = json.dumps(obj)
                except UnicodeDecodeError:
                    print("Norske bokstaver er ikke tillatt.")
                    continue
                self.send_payload(jsonobj)
                loggedOn = True
                self.hasloggedOn = True
            elif income == '-logout' and loggedOn:
                obj = {"request": "logout", "content": ""}
                try:
                    jsonobj = json.dumps(obj)
                except UnicodeDecodeError:
                    print("Norske bokstaver er ikke tillatt.")
                    continue
                self.send_payload(jsonobj)
                self.disconnect()
                self.hasloggedOn = False
            elif income == "-logout" and not loggedOn:
                print("Du må være logget inn for å kunne logge ut.")
            elif income == "-names":
                obj = {"request": "names", "content": ""}
                try:
                    jsonobj = json.dumps(obj)
                except UnicodeDecodeError:
                    print("Norske bokstaver er ikke tillatt.")
                    continue
                self.send_payload(jsonobj)

            elif income == "-history":
                self.requestHistory()
            elif income == '-Quit':
                print "Hade bra!"
                break
            elif income == '-status':
                print("Connection: "+str(self.connection))

            else:
                if not loggedOn:
                    print("Du må være logget av for å kunne chatte.")
                elif loggedOn:
                    obj = {"request": "msg", "content": income}
                    try:
                        jsonobj = json.dumps(obj)
                    except UnicodeDecodeError:
                        print("Norske bokstaver er ikke tillatt.")
                        continue
                    self.send_payload(jsonobj)

    def disconnect(self):
        self.connection.close()
        pass

    def receive_message(self, message):
        obj = json.loads(message)
        time = obj["Timestamp"]
        sender = obj["Sender"]
        response = obj["Response"]
        body = obj["Content"]

        if response == "History" and (len(body) > 1):
            for i in body:
                self.receive_message(i)
        elif response == "History" and len(body)==0:
            print '[Tid: ' + time + ']' + '[Sender: ' + sender + ']' + ' Melding: No history.'
        else:
            print '[Tid: ' + time + ']' + '[Sender: ' + sender + ']' + ' Melding: ' + body
        pass

    def send_payload(self, data):
        self.connection.send(data)
        pass

    def requestHistory(self):
        obj = {"request": "history", "content": ""}
        jsonobj = json.dumps(obj)
        self.send_payload(jsonobj)

if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    client = Client('localhost', 9998)

