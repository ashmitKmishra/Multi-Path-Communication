import os
import socket
import threading

encoded_folder = 'encoded_files'
if not os.path.exists(encoded_folder):
    os.makedirs(encoded_folder)

def start_tcp_server(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ip, port))
    s.listen(5)

    print(f"Listening for TCP connections on {ip}:{port}...")

    while True:
        c, addr = s.accept()
        print(f"Connection from {addr}")

        # Receive the file name length first
        file_name_len = int.from_bytes(c.recv(2), 'big')
        if file_name_len == 0:
            print("Received an empty file name length, closing connection.")
            c.close()
            continue
        file_name = c.recv(file_name_len).decode('utf-8')
        if not file_name:
            print("Received an empty file name, closing connection.")
            c.close()
            continue

        file_path = os.path.join(encoded_folder, file_name)
        print(f"Receiving file: {file_name}")

        # Receive the file content
        with open(file_path, 'wb') as f:
            while True:
                data = c.recv(1024)
                if not data:
                    break
                f.write(data)

        c.close()
        print(f"File {file_name} received and saved to {encoded_folder}")

if __name__ == "__main__":
    servers = [
        ('0.0.0.0', 5201),
        ('0.0.0.0', 5301),
        ('0.0.0.0', 5401)
    ]

    threads = []
    for ip, port in servers:
        t = threading.Thread(target=start_tcp_server, args=(ip, port))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
