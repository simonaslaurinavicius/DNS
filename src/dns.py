'''
    File name: dns.py
    Author: Simonas Laurinavicius
    Email: simonas.laurinavicius@mif.stud.vu.lt
    Python Version: 3.7.6

    Purpose: 
        Simple DNS Authoritative Server implementation with functionality limited to SOA, NS, MX, A, * type records. 
        Made as a study project for my Computer Networking class at Vilnius University.
'''

# Standard library
import socket 

# Local modules
import response 

def main():
    port = 1053 # DNS operates on port 53 by default, we use 1053 to mock traditional behavior
    ip = "127.0.0.1"

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # using IPv4, UDP
    sock.bind((ip, port))
    print("Listening on port 1053")
    
    while True:
        query, addr = sock.recvfrom(512) # Queries are DNS Messages which may be sent to a name server to provoke a Response 
        response_ = response.build_response(query) # Responses are DNS Messages sent back to answer the Query
        sock.sendto(response_, addr)

if __name__ == "__main__":
    main()
