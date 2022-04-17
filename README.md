# System principle

This is an implementation of the classic Practical Byzantine Fault Tolerance (PBFT) protocol proposed in 1999 by Miguel Castro and Barbara Liskov.
The user defines the number of nodes in the network and other parameters.
The clients send their requests to the network (specifically to the primary node) and the PBFT protocol starts processing the request.

# Metrics:

When a client gets its reply (f+1 similar replies), it returns the delay required to process the request and the number of exchanged messages through the network to process this request.

# Run the code:

Adjust the scenario's parameters in the main.py file (number of nodes, clients' requests, etc.), the run the code.

```
git clone https://github.com/kenzarh/PBFT
cd PBFT
python main.py
```