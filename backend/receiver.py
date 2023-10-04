import socket
import tqdm
import os
import zipfile
import subprocess

# Constants
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 5001
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

# Function to extract a zip file and run install.sh
def extract_and_install(zip_file_path, extraction_path):
    try:
        with zipfile.ZipFile(zip_file_path, 'r') as zipf:
            zipf.extractall(extraction_path)

        install_script = 'install.sh'
        prev_path = os.getcwd()
        os.chdir(extraction_path)
        if os.path.exists(install_script):
            subprocess.run(['sudo', 'bash', install_script])
            print('Installation completed successfully.')
        else:
            print('The install.sh script was not found in the extracted folder.')
        os.chdir(prev_path)
    except Exception as e:
        print(f'An error occurred: {str(e)}')

def delete_package_installation(package_path):
    prev_path = os.getcwd()
    os.chdir(package_path)
    delete_script = 'delete.sh'
    if os.path.exists(delete_script):
        subprocess.run(['sudo', 'bash', delete_script])
        print('Installation completed successfully.')
    else:
        print('The delete.sh script was not found in the extracted folder.')
    os.chdir(prev_path)

# Class to handle receiving files and commands
class Receiver:
    def __init__(self, s: socket.socket):
        self.s = s

    def receive_file(self):
        client_socket, address = self.s.accept()
        print(f"[+] {address} is connected.")

        received = client_socket.recv(BUFFER_SIZE).decode()
        filename, filesize = received.split(SEPARATOR)
        filename = os.path.basename(filename)
        filename = os.path.join('received', filename)
        filesize = int(filesize)

        progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(filename, "wb") as f:
            while True:
                bytes_read = client_socket.recv(BUFFER_SIZE)
                if not bytes_read:
                    break
                f.write(bytes_read)
                progress.update(len(bytes_read))

        client_socket.close()
        return filename

    def receive_command(self):
        client_socket, address = self.s.accept()
        received_data = client_socket.recv(BUFFER_SIZE).decode()
        command, credentials = received_data.split(SEPARATOR)
        self.send_package_list(client_socket)
        client_socket.close()
        return command, credentials

    def send_package_list(self, client_socket):
        package_list = os.listdir('packages/')
        package_list = str(package_list).encode()
        client_socket.sendall(package_list)

    def receive_package(self):
        zip_file_name = self.receive_file()
        print(f"Received: {zip_file_name}")
        package_name, ext = os.path.splitext(os.path.basename(zip_file_name))
        extraction_path = os.path.join('received_packages', package_name)
        extract_and_install(zip_file_name, extraction_path)

if __name__ == '__main__':
    if not os.path.exists('received'):
        os.makedirs('received')
    if not os.path.exists('received_packages'):
        os.makedirs('received_packages')
    with socket.socket() as s:
        s.bind((SERVER_HOST, SERVER_PORT))
        s.listen(5)
        r = Receiver(s)
        try:
            while True:
                r.receive_package()
                # command, credentials = r.receive_command()
                # print(f"Received command : {command}, credentials: {credentials}")
                # if command == 'send package':
                #     r.receive_package()
                # print(r.receive_command())
        except KeyboardInterrupt:
            r.s.close()
