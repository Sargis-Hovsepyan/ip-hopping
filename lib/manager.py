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
            
            thread = threading.Thread(target=self.handle_client, args=(client, address))
            thread.start()
            
            print(f'[ACTIVE CONNECTIONS] : {threading.activeCount() - 1}')
    
    def handle_clients(self, client, address):
        print(f"[NEW CONNECTION] : {address}")
        
        while True:
            data = client.recv(1024).decode('utf-8')
            
            if data == '!DISCONNECT':
                print(f'[{address} : Disconnected.')
                break

            response = self.process_data(data)
            client.sendall(response)
        
        # Closing the Connection.
        client.close()
    
    def process_data(self, data):
        # Process received data and return response
        # Placeholder implementation, replace with actual logic
        return b"Received: " + data