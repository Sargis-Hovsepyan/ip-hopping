import socket
import threading

class IPHopperManager:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = {}
    
    def start_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen()

        print(f"[SERVER STARTED] : {self.host}:{self.port}")

        while True:
            client, address = server.accept()
            
            thread = threading.Thread(target=self.handle_clients, args=(client, address))
            thread.start()
            
            print(f'[ACTIVE CONNECTIONS] : {threading.active_count() - 1}')
    
    def handle_clients(self, client, address):
        print(f"[NEW CONNECTION] : {address}")
        
        while True:
            data = client.recv(1024)
            
            if data.decode('utf-8') == '!DISCONNECT':
                print(f'[{address} : Disconnected.')
                break

            response = self.process_data(data)
            client.sendall(response)
        
        # Closing the Connection.
        client.close()
    
    def process_data(self, data):
        # Process received data and return response
        # Placeholder implementation, replace with actual logic
        if data:
            print("Received: " + data.decode('utf-8'))
            return b'Server Response'
        else:
            print("Error: Empty data received")
            return b'Empty data received'


if __name__ == "__main__":
    server = IPHopperManager('127.0.0.1', 5555)
    server.start_server()