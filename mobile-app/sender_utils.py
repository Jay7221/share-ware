import socket
import tqdm
import os
import zipfile
import ipaddress

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096
PACKAGE_PATH = 'packages'

PORTS = [5001]


def connect_to_server(host, port):
    try:
        s = socket.socket()
        s.settimeout(0.1)
        s.connect((host, port))
        print(f"Connected to {host}:{port}")
        return s
    except Exception as e:
        print(f"Error connecting to {host}:{port}: {str(e)}")
        return None


def send_command(command, s):
    if s:
        try:
            s.send(f"{command}".encode())
        except Exception as e:
            print(f"Error sending command: {str(e)}")


def zip_folder(folder_path, zip_file_name):
    """
    Zip a folder and its contents.

    :param folder_path: The path of the folder to be zipped.
    :param zip_file_name: The name of the zip file to create.
    """
    if not os.path.exists(folder_path):
        print(f"The package does not exist")

    try:
        with zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            print(f"Zipping {folder_path}")
            for root, dirs, files in os.walk(folder_path):
                print(root)
                print('In here')
                if not root:
                    print("Rood is None")
                for file in files:
                    file_path = os.path.join(root, file)
                    print(f'Zipping file {file_path}')
                    zipf.write(file_path, os.path.relpath(
                        file_path, folder_path))
    except Exception as e:
        raise e
        # print(f'An error occurred: {str(e)}')


def receive_message(s):
    try:
        message = s.recv(BUFFER_SIZE).decode()
        return message
    except Exception as e:
        raise e
        # print(f"Error receiving package list: {str(e)}")
        # return ""


def send_file(filename, s):
    try:
        filesize = os.path.getsize(filename)
        s.send(f"{filename}{SEPARATOR}{filesize}".encode())
        progress = tqdm.tqdm(range(
            filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)

        with open(filename, "rb") as f:
            while True:
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    break
                s.sendall(bytes_read)
                progress.update(len(bytes_read))

        return True
    except Exception as e:
        raise e
        # print(f"Error sending file {filename}: {str(e)}")
        # return False


def zip_and_send_package(package_name, s):
    folder_to_zip = os.path.join('packages', package_name)
    zip_file_name = package_name + '.zip'
    zip_folder(folder_to_zip, zip_file_name)

    if s:
        try:
            send_file(zip_file_name, s)
            print(f"Package '{package_name}' sent successfully.")
        except Exception as e:
            raise e
        os.remove(zip_file_name)


def install_package(package_name, host, port):
    try:
        command = 'INSTALL'
        s = connect_to_server(host=host, port=port)
        s.settimeout(1.0)
        send_command(command=command, s=s)
        response = receive_message(s)
        zip_and_send_package(package_name=package_name, s=s)
    except Exception as e:
        raise e
        # print(f"Exception occured: {str(e)}")
    finally:
        s.close()


def delete_package(package_name, host, port):
    command = 'DELETE'
    try:
        s = connect_to_server(host=host, port=port)
        send_command(command=command, s=s)
        response = receive_message(s)
        send_command(command=package_name, s=s)
        response = receive_message(s)
    except Exception as e:
        raise e
        # print(f"Exception occured: {str(e)}")
    finally:
        s.close()


def stop_receiver(host, port):
    command = 'QUIT'
    try:
        s = connect_to_server(host=host, port=port)
        send_command(command=command, s=s)
    except Exception as e:
        raise e
    finally:
        s.close()


def generate_ips(network_mask):
    try:
        network = ipaddress.IPv4Network(network_mask, strict=True)
        all_ips = list(map(str, network.hosts()))

        return all_ips
    except ValueError as e:
        return str(e)


def install_package_to_network(package_name, network_address, ports=PORTS):
    for ip in generate_ips(network_address):
        for port in ports:
            install_package(package_name, ip, port)


def delete_package_to_network(package_name, network_address, ports=PORTS):
    for ip in generate_ips(network_address):
        for port in ports:
            delete_package(package_name, ip, port)



if __name__ == '__main__':
    COMMANDS = ['INSTALL', 'DELETE']
    PACKAGES = os.listdir(PACKAGE_PATH)
    if not os.path.exists(PACKAGE_PATH):
        os.makedirs(PACKAGE_PATH)
    host = input("Enter host ip : ")
    if not host:
        host = '127.0.0.1'
    port = 5001

    while True:
        try:
            command = input("Enter command to send: ")
            print(PACKAGES)
            package_name = input("Enter name of package: ")
            if command == 'INSTALL':
                install_package(package_name=package_name,
                                host=host, port=port)
            elif command == 'DELETE':
                delete_package(package_name=package_name, host=host, port=port)
            else:
                break
        except Exception as e:
            print(f"Execption occred: {str(e)}")
