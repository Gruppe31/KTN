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
        print("Welcome to SuperAwesome chat. Type -help if you need assistance.")

        while True:

            income = raw_input()
            #income = unicode(rawincome, "utf-8")
            if income == '-help':
                helpCmd = ['The following commands are useful:'
                '\n -login: type "login" followed by a return, then a line consisting only of the desired username.'
                '\n -names: type only this in the console in order to retrieve all of the occupied names in the chatroom.'
                '\n -logout: type only this in the console in order to log out from the server.']
                for i in helpCmd:
                    print i
            elif income == '-login':
                print("Type in your desired username and you will be logged into the server as long as the username is not occupied.")

                income = raw_input()
                #income = unicode(rawincome, "utf-8")
                obj = {"request": "login", "content": income}
                try:
                    jsonobj = json.dumps(obj)
                except UnicodeDecodeError:
                    print("Norwegian characters are not allowed.")
                    continue
                self.send_payload(jsonobj)
                loggedOn = True
                self.hasloggedOn = True
            elif income == '-logout' and loggedOn:
                obj = {"request": "logout", "content": ""}
                try:
                    jsonobj = json.dumps(obj)
                except UnicodeDecodeError:
                    print("Norwegian characters are not allowed.")
                    continue
                self.send_payload(jsonobj)
                self.disconnect()
                self.hasloggedOn = False
            elif income == "-logout" and not loggedOn:
                print("You have to be logged in order to log out.")
            elif income == "-names":
                obj = {"request": "names", "content": ""}
                try:
                    jsonobj = json.dumps(obj)
                except UnicodeDecodeError:
                    print("Norwegian characters are not allowed.")
                    continue
                self.send_payload(jsonobj)

            elif income == "-history":
                self.requestHistory()
            elif income == '-Quit':
                print "Bye"
                break
            elif income == '-status':
                print("Connection: "+str(self.connection))

            else:
                if not loggedOn:
                    print("You have to be logged on in order to chat.")
                elif loggedOn:
                    obj = {"request": "msg", "content": income}
                    try:
                        jsonobj = json.dumps(obj)
                    except UnicodeDecodeError:
                        print("Norwegian characters are not allowed.")
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
            print '[Time: ' + time + ']' + '[Sender: ' + sender + ']' + ' Message: No history.'
        else:
            print '[Time: ' + time + ']' + '[Sender: ' + sender + ']' + ' Message: ' + body
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
    client = Client('129.241.107.140', 20000)

