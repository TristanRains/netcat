# Simple python script handling socket connections similar to netcat
# Once connected, the user can enter basic commands to be executed using subprocess, examples - pwd, whoami, ls -l

import socket, threading, subprocess, sys

def handle_client(client_socket):
    while True:
        # Receive data from the client and print the response
        data = client_socket.recv(1024).decode()
        if data:
            print(f"Received: {data}")
        # Execute the received command and send the output plus any errors back to the client
        try:
            output = subprocess.run(data.split(" "), capture_output=True, text=True)
            client_socket.send(output.stdout.encode("utf-8"))
        except subprocess.CalledProcessError as e:
            client_socket.send(e.output)
    client_socket.close()

def listen(command):
    port= command[2]
    # Create a socket object and bind for listening
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', int(port)))
    server_socket.listen(5)
    print(f"Listening on port {port}...")
    while True:
        # Accept connections whilst handling clients with threading
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

def connect(command):
    ip= command[2]
    port= command[3]
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect to the server and send messages
    client_socket.connect((ip, int(port)))
    print(f"Connected to {ip}:{port}")
    while True:
        message = input("Enter a message: ")
        client_socket.send(message.encode('utf-8'))
        data = client_socket.recv(1024).decode()
        if data:
            print(data)
    client_socket.close()

#Help menu
def help():
    print("*"*30,"\n")
    print("This script performs basic socket connections similar to netcat")
    print("It takes two commands, --listen and --connect"+"\n")
    print("--connect requires an address and a port number, eg python3 netcat.py --connect 127.0.0.1 80")
    print("--listen requires a port number, eg python3 netcat.py --listen 80")
    print("\n"+"*"*30)

#The script takes the commands --listen, -h or --connect which are handled with sys
if __name__ == "__main__":
    command= sys.argv
    if command[1]=="--listen":
        listen(command)
    elif command[1]=="--connect":
        connect(command)
    elif command[1]=="-h" or command[1]=="--help":
    	help()
    else:
        print("Invalid command. Use --listen, --connect or -h for options.")
