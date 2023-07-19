from PBFT import *
from ecc import *
import socket
import json
import time


def generate_time():
    
    return time.time()

def json_load(p):
    with open(p, 'r') as fi:
        d = json.load(fi)
    return d

def createSocket(wait,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(wait)	
    host = socket.gethostname() 
    s.bind((host, port))
    s.listen()
    
    return s

def createSocket_node(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    host = socket.gethostname() 
    s.bind((host, port))
    s.listen()
    
    return s    

def send_socket(port,req):
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname() 
    s.connect((host, port))
    s.send(req)
    
    return s
