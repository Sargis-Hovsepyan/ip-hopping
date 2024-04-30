import socket
import hashlib
import ipaddress

from hopping import ip_hopping

class TargetServer:
    def __init__(self, initial_ip, port):
        self.ip = initial_ip
        self.port = port
        self.ip_range = ipaddress.ip_network('154.168.1.0/24')

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.ip, port))
        self.server.listen(1)
    
    def start(self):
            seed = -1
            while True:
                seed = seed + 1
                print(f"[TARGET SERVER LISTENNIG ON] : {self.ip}:{self.port}")
                
                client, address = self.server.accept()
                with client:
                    print(f"[NEW CONNECTION] : {address}")

                    data = client.recv(1024)
                    if not data:
                        continue

                    # Change IP address
                    self.change_ip(data, address, seed)
    
    def change_ip(self, data, address, seed):
        client_data = data.decode('utf-8')
        last_line = client_data.split('\n')[-1]
        index = last_line.find("NIP: ")
        ip_address = last_line[index + len("NIP: "):].strip()
        
        new_ip = ip_hopping(self.ip_range, seed)
        hash_new_ip = hashlib.sha256(new_ip.encode()).hexdigest()
        
        #    self.server.close()
        #    # Create a new socket with the new IP address
        #    self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #    self.server.bind((new_ip, self.port))
        #    self.server.listen(1)
        
        # if ip_address == hash_new_ip:
        self.process_data(data, address)
        self.ip = new_ip
    
    def process_data(self, data, address):
        if data:
            print(f"[{address}]: " + data.decode('utf-8'))
        else:
            print(f"[{address}] : !EMPTY DATA")


#--------------------------------------- #
#                  MAIN                  #
#--------------------------------------- #

if __name__ == "__main__":
    server = TargetServer('localhost', 5556)
    server.start()