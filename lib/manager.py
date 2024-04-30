import socket
import hashlib
import threading
import ipaddress

from hopping import ip_hopping

class IPHopperManager:
    def __init__(self, host, port, target_initial_ip, target_port):
        self.host = host
        self.port = port

        self.target_port = target_port
        self.target_ip = target_initial_ip

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {}

        self.ip_range = ipaddress.ip_network('154.168.1.0/24')
    
    def start(self):
        self.server.bind((self.host, self.port))
        self.server.listen()

        print(f"[SERVER STARTED] : {self.host}:{self.port}")

        while True:
            client, address = self.server.accept()
            
            thread = threading.Thread(target=self.handle_clients, args=(client, address))
            thread.start()
            
            print(f'[ACTIVE CONNECTIONS] : {threading.active_count() - 1}')
    
    def handle_clients(self, client, address):
        print(f"[NEW CONNECTION] : {address}")
        
        seed = -1
        while True:
            seed = seed + 1
            data = client.recv(1024)
            
            if data.decode('utf-8') == '!DISCONNECT':
                print(f'[{address} : Disconnected.')
                break

            # Generate IP for target
            # if (seed != 0):
            #     self.tareget_ip = ip_hopping(self.ip_range, seed=seed)
            
            response = self.process_data(data, address, seed)

            # Create a new Connection
            client.close()
            
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((self.target_ip, self.target_port))
            client.sendall(response)
        
        # Closing the Connection.
        client.close()
    
    def process_data(self, data, address, seed):
        # Process received data and return response
        if data:
            new_ip = self.target_ip
            if seed != 0:
                new_ip = ip_hopping(self.ip_range, seed)
            
            print(f"[{address}]: " + data.decode('utf-8'))
            
            # Decode the received bytes into a string
            client_data = data.decode()
            
            # Hash the new IP address
            hashed_ip = hashlib.sha256(new_ip.encode()).hexdigest()
            
            # Add hashed IP to the client data
            response = client_data + "\nNIP: " + hashed_ip
            
            # Encode the processed data as bytes
            return response.encode()
        else:
            print(f"[{address}] : !EMPTY DATA")
            return data


#--------------------------------------- #
#                  MAIN                  #
#--------------------------------------- #

if __name__ == "__main__":
    server = IPHopperManager('127.0.0.1', 5555, '127.0.0.1', 5556)
    server.start()