import socket
import tqdm
import os
import zipfile
import subprocess

# Constants
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 5001
BUFFER_SIZE = 1024
SEPARATOR = "<SEPARATOR>"
PACKAGE_PATH = 'packages'

# Function to extract a zip file and run install.sh


def setup_server():
    server_socket = socket.socket()
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)
    print(f"Listening on {SERVER_HOST}:{SERVER_PORT}")
    return server_socket


def extract(zip_file_path, extraction_path):
    try:
        with zipfile.ZipFile(zip_file_path, 'r') as zipf:
            zipf.extractall(extraction_path)
    except Exception as e:
        print(f'An error occurred: {str(e)}')


def install_package(package_name):
    package_path = os.path.join(PACKAGE_PATH, package_name)
    install_script = 'install.sh'
    prev_path = os.getcwd()
    os.chdir(package_path)
    if os.path.exists(install_script):
        subprocess.run(['sudo', 'bash', install_script])
        print('Installation completed successfully.')
    else:
        print(
            f'The {install_script} script was not found in the extracted folder.')
    os.chdir(prev_path)


def delete_package(package_name):
    package_path = os.path.join(PACKAGE_PATH, package_name)
    delete_script = 'delete.sh'
    prev_path = os.getcwd()
    os.chdir(package_path)
    if os.path.exists(delete_script):
        subprocess.run(['sudo', 'bash', delete_script])
        print('Deletion completed successfully.')
    else:
        print(
            f'The {delete_script} script was not found in the extracted folder.')
    os.chdir(prev_path)


def receive_file(client_socket):

    received = client_socket.recv(BUFFER_SIZE).decode()
    filename, filesize = received.split(SEPARATOR)
    filename = os.path.basename(filename)
    filesize = int(filesize)

    progress = tqdm.tqdm(range(
        filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        while True:
            bytes_read = client_socket.recv(BUFFER_SIZE)
            if not bytes_read:
                break
            f.write(bytes_read)
            progress.update(len(bytes_read))

    return filename


def receive_command(client_socket):
    command = client_socket.recv(BUFFER_SIZE).decode()
    return command


def send_message(client_socket, message):
    client_socket.sendall(message.encode())


def receive_package(client_socket):
    zip_file_name = receive_file(client_socket=client_socket)
    print(f"Received: {zip_file_name}")
    package_name, ext = os.path.splitext(os.path.basename(zip_file_name))
    extraction_path = os.path.join('packages', package_name)
    extract(zip_file_name, extraction_path)
    os.remove(zip_file_name)
    install_package(package_name=package_name)


if __name__ == '__main__':
    if not os.path.exists(PACKAGE_PATH):
        os.makedirs(PACKAGE_PATH)
    s = setup_server()
    try:
        while True:
            client_socket, address = s.accept()
            command = receive_command(client_socket=client_socket)
            print(f"Command received: {command}")
            send_message(client_socket=client_socket, message="<OK>")
            if command == 'INSTALL':
                receive_package(client_socket)
            
            if command == 'DELETE':
                package_name = receive_command(client_socket=client_socket)
                send_message(client_socket=client_socket, message="<OK>")
                delete_package(package_name=package_name)

            client_socket.close()

            if command == 'QUIT':
                break

    except Exception as e:
        print(f"Exception occured: {str(e)}")
    finally:
        s.close()
