from PBFT import *
from client import *

import threading

# Parameters to be defined by the user

waiting_time_before_resending_request = 3 # Time the client will wait before resending the request. This time, it broadcasts the request to all nodes
timer_limit_before_view_change = 4 # There is no value proposed in the paper so let's fix it to 20s
checkpoint_frequency = 100 # 100 is the proposed value in the original article

# Running PBFT protocol
run_PBFT(number_of_honest_nodes=4,number_of_non_responding_nodes=0,number_of_faulty_primary=0,number_of_slow_nodes=0,checkpoint_frequency0=checkpoint_frequency,clients_ports0=clients_ports,timer_limit_before_view_change0=timer_limit_before_view_change)

# Lancer différents clients, pas de requête pour un même client pour l'instant (fonctionnalité à ajouter,) / ajouter un join pour exécuter une autre requête
primary_node_id = get_primary_id()
nodes_ids_list=get_nodes_ids_list()
f= get_f()

C0=Client(0,waiting_time_before_resending_request)
threading.Thread(target=C0.send_to_primary,args=("I am the client 0",primary_node_id,nodes_ids_list,f)).start()

#C1=Client(1,waiting_time_before_resending_request)
#threading.Thread(target=C1.send_to_primary,args=("I am the client 1",primary_node_id,nodes_ids_list,f)).start()

#C2=Client(2,waiting_time_before_resending_request)
#threading.Thread(target=C2.send_to_primary,args=("I am the client 2",primary_node_id,nodes_ids_list,f)).start()