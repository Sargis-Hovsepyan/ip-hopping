import socket
import threading
import time
from hopping import ip_hopping
import ipaddress

class Router:
    def __init__(self, host, port, ip_range):
        self.host = host
        self.port = port
        self.ip_range = ip_range
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()
        
        self.routing_table = {} 
        self.active_connections = {} 

        self.lock = threading.Lock() 
    
    def start(self):
        print(f"[ROUTER STARTED] : {self.host}:{self.port}")

        while True:
            client, address = self.server.accept()
            print(f"[NEW CONNECTION] : {address}")

            thread = threading.Thread(target=self.handle_client, args=(client, address))
            thread.start()

    def handle_client(self, client, address):
        with self.lock:
            if address[0] not in self.routing_table:
                new_ip = ip_hopping(self.ip_range)
                self.routing_table[address[0]] = new_ip
                print(f"[ROUTING] : {address} => {new_ip}")

            target_ip = self.routing_table[address[0]]
            target_port = self.port

            try:
                data = client.recv(1024)
                if data:
                    print(f"[RECEIVED] from {address}: {data.decode('utf-8')}")
                    self.route_traffic(data, target_ip, target_port)
            finally:
                client.close()

    def route_traffic(self, data, target_ip, target_port):
        with self.lock:
            if target_ip in self.active_connections:
                connection = self.active_connections[target_ip]
            else:
                connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                connection.connect((target_ip, target_port))
                self.active_connections[target_ip] = connection

        connection.sendall(data)
        print(f"[SENT] to {target_ip}: {data.decode('utf-8')}")

    def stop(self):
        with self.lock:
            for connection in self.active_connections.values():
                connection.close()
            self.active_connections.clear()
        self.server.close()
        print("[ROUTER STOPPED]")

