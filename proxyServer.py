from socket import *
import sys



# Return received HTTP message that is stored in tuple (lines, data_message), where
# lines is a list of request/status line plus header lines, and data_message is the byte data
# after "\r\n\r\n"
def receive_http_message(from_socket, is_response_for_get = False):
    # Read message until "\r\n\r\n" or empty message is received
    message = from_socket.recv(2048) # Fill in start # Fill in end
    #print(message.decode())
    while "\r\n\r\n".encode() not in message and len(message)>0:
        message += from_socket.recv(2048) # Fill in start # Fill in end

    text_message, crlf, data_message = message.partition("\r\n\r\n".encode())

    # Divide text part into lines
    lines = text_message.decode().split("\r\n")
    #print(lines)
    content_length = None
    lengths = '' 
    # Find if the value of content length is provided
    for line in lines:
        #print(line)
        if "Content-Length" in line:
            lengths = line.split(":")
            content_length = int(lengths[1])
            break 
    # Fill in start
    # Fill in end

    if content_length != None:
        # Keep reading data message until the number of bytes indicated by content
        #length is received
        while content_length - len(data_message)>0:
            data_message += from_socket.recv(2048)# Fill in start # Fill in end
            
    elif is_response_for_get and ("200 OK" in lines[0] or "404 Not Found" in lines[0]):
        # No content length but it is a response message with data content, so keep
        #reading remainder and attach it to data message
        remained_data_message = from_socket.recv(2048) # Fill in start # Fill in end
        while len(remained_data_message)>0:
            data_message += remained_data_message
            remained_data_message = from_socket.recv(2048)# Fill in start # Fill in end

    return (lines, data_message)
# Get host name and port number from the request line, and update the path name of
#the request line
def get_host_name_port_and_update_request_line(message):
    request = message[0].split()
    host_name = request[1].partition("//")[2]
    #print(host_name)
    if host_name == "":
        host_name = request[1][1:]
    #print(host_name)
    host_name, slash, path_name = host_name.partition("/")
    # Update the path name of the request line
    request[1] = "/"+path_name

    message[0] = " ".join(request)
    

    # Get the port number
    if ":" in host_name:
        port = host_name.split(":")[1]# Fill in start # Fill in end
        host_name = host_name.split(":")[0]
                
    else:
        port = 80# Fill in start # Fill in end
        
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
    
server_socket.bind(("", int(sys.argv[2])))
server_socket.listen(1)
# Fill in start
# Fill in end
while True:
    # Strat receiving data from the client
    print('Ready to serve...')

    client_socket, addr = server_socket.accept()
    print('Received a connection from:', addr)

    connection_socket = None
    try:
        # Receive request message from the client
        request_message =  receive_http_message(client_socket, False) #client_socket.recv(2048).decode()# Fill in start # Fill in ends
        
        #print(request_message)

        if request_message[0][0] == "":
            raise TimeoutError("Nothing is received from Client")

        # Get host name and port number for the web server from the request
        # message and update the path name of the request line
        
        host_name, port = get_host_name_port_and_update_request_line(request_message[0]) # Fill in start # Fill in end
        #print(request_message[0])
        print('Connecting to ', host_name,' at ' , port, ' ', request_message[0][1])
        # Create connection_socket and connect it to the web server
        connection_socket = socket(AF_INET, SOCK_STREAM)# Fill in start # Fill in end
 
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
        
        #print(len(response_message[1]))

        # Send the response message to the client
        # Fill in start
        send_http_message(response_message, client_socket)
        #client_socket.sendall(response_message[1])
        # Fill in end
        connection_socket.close()
    except Exception as exception:
        print(exception)
    # Close socket connections to the client and the web server (if any)
    # Fill in start
    client_socket.close()
    # Fill in end

        
        
        
        