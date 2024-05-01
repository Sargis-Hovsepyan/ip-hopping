import socket
import hashlib
import threading
import ipaddress
import random

from hopping import ip_hopping
from router import Router


class IPHopperManager:
    def __init__(self, host, port, target_initial_ip, target_port, routers):
        self.host = host
        self.port = port

        self.target_port = target_port
        self.target_ip = target_initial_ip

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {}

        self.ip_range = ipaddress.ip_network('154.168.1.0/24')
        self.routers = routers

    def start(self):
        self.server.bind((self.host, self.port))
        self.server.listen()

        print(f"[SERVER STARTED] : {self.host}:{self.port}")

        while True:
            client, address = self.server.accept()

            thread = threading.Thread(
                target=self.handle_clients, args=(client, address))
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

            response = self.process_data(data, address, seed)
            self.send_to_router(response)

        # Closing the Connection.
        client.close()

    def send_to_target(self, message, ip, port):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, port))
        client.sendall(message)

        client.close()

    def send_to_router(self, message):
        router = random.choice(self.routers)

        router_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        router_client.connect((router[0], router[1]))
        router_client.sendall(message)
        router_client.close()

    def process_data(self, data, address, seed):
        # Process received data and return response
        if not data:
            print(f"[{address}] : !EMPTY DATA")
            return data

        new_ip = self.target_ip
        if seed != 0:
            new_ip = ip_hopping(self.ip_range, seed)

        print(f"[{address}]: " + data.decode('utf-8'))

        # Decode the received bytes into a string
        client_data = data.decode()

        # Hash the new IP address
        hashed_ip = hashlib.sha256(new_ip.encode()).hexdigest()

        # Add hashed IP to the client data
        response = client_data + "\nNIP: " + hashed_ip + "#" + str(seed)

        # Encode the processed data as bytes
        return response.encode()


# --------------------------------------- #
#                  MAIN                  #
# --------------------------------------- #

if __name__ == "__main__":

    # Create at least one router
    routers = []

    address = ['127.0.0.1', 7000]
    routers.append(address)

    server = IPHopperManager('127.0.0.1', 5555, '127.0.0.1', 5556, routers)
    server.start()
