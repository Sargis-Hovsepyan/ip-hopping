import socket
import threading
import time
from hopping import ip_hopping
import ipaddress


class Router:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.ip_range = ipaddress.ip_network('154.168.1.0/24')

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()

        self.routing_table = []
        self.active_connections = {}

        self.ip = None

    def start(self):
        print(f"[ROUTER STARTED] : {self.host}:{self.port}")

        while True:
            client, address = self.server.accept()
            print(f"[NEW CONNECTION] : {address}")

            thread = threading.Thread(
                target=self.handle_client, args=(client, address))
            thread.start()

    def handle_client(self, client, address):
        rt = next(
            (route for route in self.routing_table if route["source"] == '127.0.0.1:5555'), None)
        target_ip = rt['destination'].split(":")[0]
        target_port = rt['destination'].split(":")[1]
        ip = target_ip

        print(f"[ROUTING] : {address} => {target_ip}")

        try:
            data = client.recv(1024)
            if data:
                print(f"[RECEIVED] from {address}: {data.decode('utf-8')}")
                self.route_traffic(data, target_ip, target_port)
        finally:
            client.close()

    def route_traffic(self, data, target_ip, target_port):
        print("Getting here")
        print("or here")
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("or there")
        connection.connect((target_ip, int(target_port)))
        print("at leas connected")
        self.active_connections[target_ip] = connection

        connection.sendall(data)
        print(f"[SENT] to {self.ip}: {data.decode('utf-8')}")

    def stop(self):
        for connection in self.active_connections.values():
            connection.close()
        self.active_connections.clear()
        self.server.close()
        print("[ROUTER STOPPED]")

# --------------------------------------- #
#                  MAIN                   #
# --------------------------------------- #


if __name__ == "__main__":
    router = Router('127.0.0.1', 7000)

    address = {'source': '127.0.0.1:5555', 'destination': '127.0.0.1:5556'}
    router.routing_table.append(address)

    router.start()
