from PBFT import *
from client import *

import threading
import time

# Parameters to be defined by the user

waiting_time_before_resending_request = 200 # Time the client will wait before resending the request. This time, it broadcasts the request to all nodes
timer_limit_before_view_change = 200 # There is no value proposed in the paper so let's fix it to 120s
checkpoint_frequency = 100 # 100 is the proposed value in the original article

# Define the nodes we want in our network + their starting time + their type
nodes={} # This is a dictionary of nodes we want in our network. Keys are the nodes types, and values are a list of tuples of starting time and number of nodes 
#nodes[starting time] = [(type of nodes , number of nodes)]
nodes[0]=[("faulty_primary",0),("slow_nodes",0),("honest_node",4),("non_responding_node",0),("faulty_node",0),("faulty_replies_node",0)] # Nodes starting from the beginning
#nodes[1]=[("faulty_primary",0),("honest_node",1),("non_responding_node",0),("slow_nodes",1),("faulty_node",1),("faulty_replies_node",0)] # Nodes starting after 2 seconds
#nodes[2]=[("faulty_primary",0),("honest_node",0),("non_responding_node",0),("slow_nodes",2),("faulty_node",1),("faulty_replies_node",0)]

# Running PBFT protocol
run_APBFT(nodes=nodes,proportion=1,checkpoint_frequency0=checkpoint_frequency,clients_ports0=clients_ports,timer_limit_before_view_change0=timer_limit_before_view_change)

time.sleep(1) # Waiting for the network to start...

# Run clients:
requests_number = 1  # The user chooses the number of requests he wants to execute simultaneously (They are all sent to the PBFT network at the same time) - Here each request will be sent by a different client
clients_list = []
for i in range (requests_number):
    globals()["C%s" % str(i)]=Client(i,waiting_time_before_resending_request)
    clients_list.append(globals()["C%s" % str(i)])
for i in range (requests_number):
    threading.Thread(target=clients_list[i].send_to_primary,args=("I am the client "+str(i),get_primary_id(),get_nodes_ids_list(),get_f())).start()
    time.sleep(0) #Exécution plus rapide lorsqu'on attend un moment avant de lancer la requête suivante