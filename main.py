from PBFT import *
from client import *

import threading
import time

# Parameters to be defined by the user

waiting_time_before_resending_request = 60 # Time the client will wait before resending the request. This time, it broadcasts the request to all nodes
timer_limit_before_view_change = 60 # There is no value proposed in the paper so let's fix it to 20s
checkpoint_frequency = 100 # 100 is the proposed value in the original article

# Define the nodes we want in our network + their starting time + their type
nodes={} # This is a dictionary of nodes we want in our network. Keys are the nodes types, and values are a list of tuples of starting time and number of nodes 
#nodes[starting time] = [(type of nodes , number of nodes)]
nodes[0]=[("honest_node",20),("non_responding_node",0),("faulty_primary",0),("slow_nodes",0)] # Nodes starting from the beginning
nodes[1]=[("honest_node",0),("non_responding_node",0),("faulty_primary",0),("slow_nodes",0)] # Nodes starting after 2 seconds

# Running PBFT protocol
run_PBFT(nodes=nodes,checkpoint_frequency0=checkpoint_frequency,clients_ports0=clients_ports,timer_limit_before_view_change0=timer_limit_before_view_change)

time.sleep(2) # Waiting for the network to start...

# Lancer différents clients, pas de requête pour un même client pour l'instant (fonctionnalité à ajouter,) / ajouter un join pour exécuter une autre requête
primary_node_id = get_primary_id()
nodes_ids_list=get_nodes_ids_list()
f= get_f()

requests_number =1  # The user chooses the number of requests he wants to execute simultaneously (They are all sent to the PBFT network at the same time) - Here each request will be sent by a different client
clients_list = []
for i in range (requests_number):
    globals()["C%s" % str(i)]=Client(i,waiting_time_before_resending_request)
    clients_list.append(globals()["C%s" % str(i)])
for i in range (requests_number):
    threading.Thread(target=clients_list[i].send_to_primary,args=("I am the client "+str(i),primary_node_id,nodes_ids_list,f)).start()
    time.sleep(2) #Exécution plus rapide lorsqu'on attend un moment avant de lancer la requête suivante