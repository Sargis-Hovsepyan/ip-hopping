import socket

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = None

    def close_connection(self):
        if self.client_socket:
            self.client_socket.close()
    
    def connect(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            self.connected = True
            print("Connected to server.")
        except ConnectionRefusedError:
            print("Connection refused. Server may be down.")
        except Exception as e:
            print(f"Error occurred during connection: {e}") 
   

    def send_message(self, message):
        if not self.connected:
            print("Not connected to server.")
            return

        try:
            self.client_socket.sendall(message.encode('utf-8'))
            print("Message sent successfully.")
        except ConnectionAbortedError:
            print("Connection aborted. Reconnecting...")
            self.connect()
            self.send_message(message)
        except Exception as e:
            print(f"Error occurred while sending message: {e}")



if __name__ == "__main__":
    host = "localhost"
    port = 5555

    client = Client(host, port)
    client.connect()

    while True:
        message = input("Enter message to send: ")
        client.send_message(message)

        if message == '!DISCONNECT':
            break
    
    client.close_connection()
