import socket
import hashlib
import ipaddress

from hopping import ip_hopping


class TargetServer:
    def __init__(self, initial_ip, port):
        self.host = initial_ip
        self.port = port
        self.ip_hopped = initial_ip
        self.ip_range = ipaddress.ip_network('154.168.1.0/24')

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.server.bind((self.host, self.port))
        self.server.listen(1)

        seed = -1
        while True:
            seed = seed + 1
            print(
                f"[TARGET SERVER LISTENNIG ON] : {self.ip_hopped}:{self.port}")

            client, address = self.server.accept()
            with client:
                print(f"[NEW CONNECTION] : {address}")

                data = client.recv(1024)
                if not data:
                    continue

                # Change IP address
                response, process = self.change_ip(data, address, seed)
                if (process):
                    self.process_data(response, address)
                else:
                    print(
                        f"[TARGET SERVER]: Mismatch of IP Sent by Manager: Refusing to Process!")

    def change_ip(self, data, address, seed):
        client_data = data.decode('utf-8')
        process = False

        last_line = client_data.split('\n')[-1]
        ip_address = last_line[len("NIP: "):].strip()

        new_ip = self.host
        if seed != 0:
            new_ip = ip_hopping(self.ip_range, seed)

        hash_new_ip = hashlib.sha256(new_ip.encode()).hexdigest()
        self.ip_hopped = new_ip

        if ip_address == hash_new_ip:
            process = True

        print("ip_address: " + ip_address)
        print("new_ip_address: " + hash_new_ip)

        return client_data[:client_data.index("NIP:")].encode(), process

    def process_data(self, data, address):
        if data:
            print(f"[{address}]: " + data.decode('utf-8'))
        else:
            print(f"[{address}] : !EMPTY DATA")


# --------------------------------------- #
#                  MAIN                  #
# --------------------------------------- #

if __name__ == "__main__":
    server = TargetServer('127.0.0.1', 5556)
    server.start()
