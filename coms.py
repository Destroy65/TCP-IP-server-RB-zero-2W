import socket
import threading

HOST = '0.0.0.0'  # Listen on all available interfaces
PORT = 6420
clients = {}      # Dictionary to store client connections

logData = False

def handle_client(client_socket, client_address):
    while True:
        try:
            # Receive data from the client
            data = client_socket.recv(100)
            if not data:
                break
            
            # Print received data and address
            if logData: print(f"Received data from {client_address}: {data}")
            
            for addr, sock in clients.items():
                if addr != client_address:
                    sock.send(data)
        except:
            break

    # Remove the client from the dictionary and close the socket
    del clients[client_address]
    client_socket.close()

def start_server(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, client_address = server.accept()
        print(f"Accepted connection from {client_address}")
        clients[client_address] = client_socket

        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()

if __name__ == "__main__":
    start_server(HOST, PORT)