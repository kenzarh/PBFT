import threading
import time

import config
from client import Client
from PBFT import (get_f, get_nodes_ids_list, get_primary_id, run_PBFT)

# Running PBFT protocol
run_PBFT(nodes=config.nodes,
         proportion=1,
         checkpoint_frequency0=config.checkpoint_frequency,
         clients_ports0=None,  # This will be handled by the PBFT network
         timer_limit_before_view_change0=config.timer_limit_before_view_change)

time.sleep(1) # Waiting for the network to start...

# Run clients:
requests_number = 1
clients_list = []
for i in range (requests_number):
    client = Client(i, config.waiting_time_before_resending_request)
    clients_list.append(client)

for i, client in enumerate(clients_list):
    threading.Thread(target=client.send_to_primary,args=("I am the client "+str(i),get_primary_id(),get_nodes_ids_list(),get_f())).start()
    time.sleep(0)