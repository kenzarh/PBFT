import datetime
import json
import socket
import time

from ecc import generate_signature, generate_verfiy
from PBFT import reply_received
from utils import createSocket, json_load, send_socket


ports_file = "ports.json"
ports=json_load(ports_file)

clients_starting_port = ports["clients_starting_port"]
clients_max_number = ports["clients_max_number"]

nodes_starting_port = ports["nodes_starting_port"]
nodes_max_number = ports["nodes_max_number"]

nodes_ports = [(nodes_starting_port + i) for i in range (0,nodes_max_number)]
clients_ports = [(clients_starting_port + i) for i in range (0,clients_max_number)]

global request_format_file
request_format_file = "messages_formats/request_format.json"

class Client:

    def __init__(self,client_id,waiting_time_before_resending_request):
        self.client_id = client_id
        self.client_port = clients_ports[client_id]
        port=self.client_port
        s = createSocket(waiting_time_before_resending_request,port)
        self.socket = s
        self.sent_requests_without_answer=[]

    def broadcast_request(self,request_message,nodes_ids_list,sending_time,f):

        for node_id in nodes_ids_list:
            node_port = nodes_ports[node_id]
            send_socket(node_port,request_message)

        answered_nodes = []
        similar_replies = 0
        replies={}
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
            received_message = c.recv(2048)
        
            [received_message,public_key] = received_message.split(b'split')
  
            received_message  =generate_verfiy(public_key,received_message)
            received_message = received_message.replace("\'", '"')
            received_message = json.loads(received_message)
            answering_node_id = received_message["node_id"]
            request_timestamp = received_message["timestamp"]
            result = received_message["result"]
            response = [request_timestamp,result]
            str_response = str(response)

            if (answering_node_id not in answered_nodes):
                answered_nodes.append(answering_node_id)
                if str_response not in replies:
                    replies[str_response] = 1
                else:
                    replies[str_response] = replies[str_response] + 1
                if (replies[str_response]>similar_replies):
                    similar_replies = similar_replies +1
                    if similar_replies == (f+1):
                    
                        receiving_time=time.time()
                        duration = receiving_time-sending_time
                        number_of_messages = reply_received(received_message["request"],received_message["result"])
                        print("Client %d got reply within %f seconds. The network exchanged %d messages" % (self.client_id,duration,number_of_messages))
                        self.sent_requests_without_answer.remove(received_message["request"])

    def send_to_primary (self,request,primary_node_id,nodes_ids_list,f):
        primary_node_port = nodes_ports[primary_node_id]
        request_message=json_load(request_format_file)
        now = datetime.datetime.now().timestamp()
        request_message["timestamp"] = now
        request_message["request"] = request
        request_message["client_id"] = self.client_id
        request_message = generate_signature(request_message)
        send_socket(primary_node_port,request_message)
        if (request not in self.sent_requests_without_answer):
            self.sent_requests_without_answer.append(request)
        sending_time = time.time()
        answered_nodes = []
        similar_replies = 0
        replies={}
        nodes_replies={}
        s = self.socket

        while True:
            try: 
                s=self.socket
                sender_socket = s.accept()[0]
            except socket.timeout:
                if len(self.sent_requests_without_answer)!=0:
                    print("No received reply")
                    self.broadcast_request(request_message,nodes_ids_list,sending_time,f)
                    break
                else:
                    continue
            received_message = sender_socket.recv(2048)
            
            sender_socket.close()
        
            [received_message , public_key] = received_message.split(b'split')
  
            received_message  = generate_verfiy(public_key,received_message)
            received_message = received_message.replace("\'", '"')
            received_message = json.loads(received_message)
            answering_node_id = received_message["node_id"]
            request_timestamp = received_message["timestamp"]
            result = received_message["result"]
            response = [request_timestamp,result]
            str_response = str(response)

            if (answering_node_id not in answered_nodes):
                answered_nodes.append(answering_node_id)
                nodes_replies[answering_node_id] = str_response
                if str_response not in replies:
                    replies[str_response] = 1
                else:
                    replies[str_response] = replies[str_response] +1
                if (replies[str_response]>similar_replies):
                    similar_replies = similar_replies +1
                if similar_replies >= (f+1):
                        
                        receiving_time=time.time()
                        duration = receiving_time-sending_time
                        number_of_messages = reply_received(received_message["request"],received_message["result"])
                        if similar_replies == (f+1):
                            print("Client %d got reply within %f seconds. The network exchanged %d messages" % (self.client_id,duration,number_of_messages))
                        if (received_message["request"] in self.sent_requests_without_answer):
                            self.sent_requests_without_answer.remove(received_message["request"])