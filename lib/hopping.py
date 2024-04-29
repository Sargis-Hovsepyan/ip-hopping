import time
import numpy as np
import ipaddress

def ip_hopping(ip_range, seed=42):
  # Use a statistical distribution based on timestamp
    # Here, we use a simple linear mapping between timestamp and IP index
    timestamp = int(time.time())
    np.random.seed(seed + timestamp)  # Adjust the seed based on the timestamp

    ip_addresses = list(ipaddress.ip_network(ip_range).hosts())
    probabilities = np.random.dirichlet(np.ones(len(ip_addresses)))
    
    # Choose an IP address based on the probabilities
    new_ip = str(np.random.choice(ip_addresses, p=probabilities))
    
    return new_ip
