import socket
import os

def send_file(file_path, ip, port):
    try:
        print(f"Trying to open file: {file_path}")  # Debug statement
        if not os.path.exists(file_path):
            print(f"File does not exist: {file_path}")
            return

        file_name = os.path.basename(file_path)
        file_name_len = len(file_name)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, port))
            # Send the file name length and file name first
            s.sendall(file_name_len.to_bytes(2, 'big'))
            s.sendall(file_name.encode('utf-8'))

            # Send the file content
            with open(file_path, 'rb') as f:
                while True:
                    data = f.read(1024)
                    if not data:
                        break
                    s.sendall(data)

            print(f"{file_path} sent to {ip}:{port}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

files_and_paths = [
    ('/home/multipath1/Documents/ue_server/encoded_files/video1.mp4', '10.45.1.7', 5201),
    ('/home/multipath1/Documents/ue_server/encoded_files/video2.mp4', '10.45.2.8', 5301),
    ('/home/multipath1/Documents/ue_server/encoded_files/video3.mp4', '10.45.3.9', 5401)
]

print(f"Current working directory: {os.getcwd()}")

for file_path, ip, port in files_and_paths:
    print(f"Attempting to send file: {file_path} to {ip}:{port}")
    send_file(file_path, ip, port)
