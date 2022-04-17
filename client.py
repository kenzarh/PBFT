import socket
import json
import datetime
import time
from PBFT import *

nodes_ports = [(2000 + i) for i in range (0,2000)]

clients_ports = [(20000 + i) for i in range (0,1000)]

global request_format_file
request_format_file = "request_format.json"

class Client: # Client's communication is synchronous: It can not send a request until its last request is answered.

    def __init__(self,client_id,waiting_time_before_resending_request):
        self.client_id = client_id
        self.client_port = clients_ports[client_id]
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(waiting_time_before_resending_request)	
        host = socket.gethostname() 
        s.bind((host, self.client_port))
        s.listen()
        self.socket = s
        self.sent_requests_without_answer=[] # Requests the client sent but didn't get an answer yet

    def broadcast_request(self,request_message,nodes_ids_list,sending_time,f): # This function is executed if the primary node doesn't receive the request. It is then broadcasted to all the nodes

        for node_id in nodes_ids_list:
            node_port = nodes_ports[node_id]
            sending_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            host = socket.gethostname() 
            sending_socket.connect((host, node_port))
            sending_socket.send(str(request_message).encode())

        # Waiting for answers
        answered_nodes = [] # list of nodes ids that answered the request
        similar_replies = 0 # Initiate the number of similar replies to 0 then takes the max ...
        replies={} # A dictionary of replies, keys have the form:[timestamp,result] and the values are the number of time this reply was received
        s = self.socket
        while True:
            try: 
                c,_ = s.accept()
            except socket.timeout:
                if len(self.sent_requests_without_answer)!=0:
                    print("No received reply")
                    self.broadcast_request(request_message,nodes_ids_list,sending_time,f)
                    break
                else:
                    break
            received_message = c.recv(2048).decode()
            received_message = received_message.replace("\'", "\"")
            received_message = json.loads(received_message)
            #print("Client %d received message: %s" % (self.client_id , received_message))
            answering_node_id = received_message["node_id"]
            request_timestamp = received_message["timestamp"]
            result = received_message["result"]
            response = [request_timestamp,result]
            str_response = str(response)
            # TO DO : S'assurer de la signature du message
            if (answering_node_id not in answered_nodes): # Ne rien faire si le noeud a déjà répondu
                answered_nodes.append(answering_node_id)
                # Increment the number of received replies:
                if str_response not in replies:
                    replies[str_response] = 1
                else:
                    replies[str_response] = replies[str_response] + 1
                if (replies[str_response]>similar_replies):
                    similar_replies = similar_replies +1
                    if similar_replies == (f+1):
                        receiving_time=time.time()
                        duration = receiving_time-sending_time
                        number_of_messages = stop_request_execution(received_message["request"])
                        print("Client %d got reply within %f seconds. The network exchanged %d messages" % (self.client_id,duration,number_of_messages))
                        self.sent_requests_without_answer.remove(received_message["request"])
                        #s.close()
                        #sys.exit()

    def send_to_primary (self,request,primary_node_id,nodes_ids_list,f): # Sends a request to the primary and waits for f+1 similar answers
        primary_node_port = nodes_ports[primary_node_id]
        with open(request_format_file):
            request_format= open(request_format_file)
            request_message = json.load(request_format)
            request_format.close()
        now = datetime.datetime.now().timestamp()
        request_message["timestamp"] = now
        request_message["request"] = request
        request_message["client_id"] = self.client_id
        # The client sends the request to what it believes is the primary node:
        sending_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostname() 
        sending_socket.connect((host, primary_node_port))
        sending_socket.send(str(request_message).encode())
        if (request not in self.sent_requests_without_answer):
            self.sent_requests_without_answer.append(request)
        sending_time = time.time() # This is the time when the client's request was sent to the network
        answered_nodes = [] # list of nodes ids that answered the request
        similar_replies = 0 # Initiate the number of similar replies to 0 then takes the max ...
        replies={} # A dictionary of replies, keys have the form:[timestamp,result] and the values are the number of time this reply was received
        s = self.socket
        while True:
            try: 
                c, addr = s.accept()
            except socket.timeout:
                if len(self.sent_requests_without_answer)!=0:
                    print("No received reply")
                    # Broadcasting request:
                    self.broadcast_request(request_message,nodes_ids_list,sending_time,f)
                    break
                else:
                    continue
            received_message = c.recv(2048).decode()
            received_message = received_message.replace("\'", "\"")
            received_message = json.loads(received_message)
            #print("Client %d received message: %s" % (self.client_id , received_message))
            answering_node_id = received_message["node_id"]
            request_timestamp = received_message["timestamp"]
            result = received_message["result"]
            response = [request_timestamp,result]
            str_response = str(response)
            # TO DO : S'assurer de la signature du message
            if (answering_node_id not in answered_nodes): # Ne rien faire si le noeud a déjà répondu
                answered_nodes.append(answering_node_id)
                # Increment the number of received replies:
                if str_response not in replies:
                    replies[str_response] = 1
                else:
                    replies[str_response] = replies[str_response] +1
                if (replies[str_response]>similar_replies):
                    similar_replies = similar_replies +1
                    if similar_replies == (f+1):
                        receiving_time=time.time()
                        duration = receiving_time-sending_time
                        number_of_messages = stop_request_execution(received_message["request"])
                        print("Client %d got reply within %f seconds. The network exchanged %d messages" % (self.client_id,duration,number_of_messages))
                        self.sent_requests_without_answer.remove(received_message["request"])
                        #s.close()
                        #sys.exit()