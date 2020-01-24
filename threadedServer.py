#import socket module
from socket import *
import threading
import sys

def receive_http_message(from_socket, is_response_for_get = False):
   
    message = from_socket.recv(2048) 
    while "\r\n\r\n".encode() not in message and len(message)>0:
        message += from_socket.recv(2048) 

    text_message, crlf, data_message = message.partition("\r\n\r\n".encode())

    lines = text_message.decode().split("\r\n")
    
    content_length = None
    lengths = '' 
    
    for line in lines:
        if "Content-Length" in line:
            lengths = line.split(":")
            content_length = int(lengths[1])
            break 


    if content_length != None:

        while content_length - len(data_message)>0:
            data_message += from_socket.recv(2048)
            
    elif is_response_for_get and ("200 OK" in lines[0] or "404 Not Found" in lines[0]):
        # No content length but it is a response message with data content, so keep
        #reading remainder and attach it to data message
        remained_data_message = from_socket.recv(2048)
        while len(remained_data_message)>0:
            data_message += remained_data_message
            remained_data_message = from_socket.recv(2048)

    return (lines, data_message)
# Get host name and port number from the request line, and update the path name of
#the request line
def get_host_name_port_and_update_request_line(message):
    request = message[0].split()

    host_name = request[1].partition("//")[2]

    if host_name == "":
        host_name = request[1][1:]

    host_name, slash, path_name = host_name.partition("/")
    # Update the path name of the request line
    request[1] = "/"+path_name

    message[0] = " ".join(request)
    

    # Get the port number
    if ":" in host_name:
        port = host_name.split(":")[1]
        host_name = host_name.split(":")[0]
                
    else:
        port = 80
        
    #message[1] = message[1].replace(message[1], "Host: " + host_name)
    return host_name, port
#Send HTTP message that is stored in tuple (lines, data_message), where lines is a 
#list of request/status line plus header lines, and data_message is the byte data after
#header lines
def send_http_message(message, to_socket):
    for line in message[0]:
        head = line + "\r\n"
        to_socket.send(head.encode())
    to_socket.send("\r\n".encode() + message[1])

if len(sys.argv) != 3:
    print('Usage : "python ProxyServer.py server_ip server_port"')
    sys.exit(2)

# Create a server socket, bind it to a port and start listening
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('', int(sys.argv[2])))


class clientThread(threading.Thread):
    def __init__(self, csocket,caddr ):
        threading.Thread.__init__(self)
        self.s = csocket
        self.a = caddr
    def run(self):
        connection_socket = None
        try:
            # Receive request message from the client
            request_message =  receive_http_message(self.s, False) #client_socket.recv(2048).decode()# Fill in start # Fill in ends
            
            #print(request_message)
    
            if request_message[0][0] == "":
                raise TimeoutError("Nothing is received from Client")
            # Get host name and port number for the web server from the request
            # message and update the path name of the request line
            
            host_name, port = get_host_name_port_and_update_request_line(request_message[0]) # Fill in start # Fill in end
            print('Connecting to ', host_name,' at ' , port, ' ', request_message[0][1])
            #print('Connecting to ', host_name,' at ' , port)
            # Create connection_socket and connect it to the web server
            connection_socket = socket(AF_INET, SOCK_STREAM)
     
            # Fill in start
            connection_socket.connect((host_name,int(port)))
            # Fill in end
    
            # Send the request message to the web server
            # Fill in start
            #print(request_message)
            send_http_message(request_message, connection_socket)
            # Fill in end
    
            # Receive response message from the web server
            response_message = receive_http_message(connection_socket, True)
            
            #print(response_message)
    
            # Send the response message to the client
            send_http_message(response_message, self.s)
            #self.s.sendall(response_message[1])

            connection_socket.close()
        except Exception as exception:
            print(exception)
        # Close socket connections to the client and the web server (if any)
        self.s.close()

while True:
    server_socket.listen(2)
    #Establish the connection
    print('Ready to serve...')

    connectionSocket, addr = server_socket.accept()#Fill in start #Fill in end
    print('Received a connection from:', addr)
    newThread = clientThread(connectionSocket, addr)
    newThread.start()
server_socket.close()
