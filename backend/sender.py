import socket
import tqdm
import os
import zipfile

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096

def zip_folder(folder_path, zip_file_name):
    """
    Zip a folder and its contents.

    :param folder_path: The path of the folder to be zipped.
    :param zip_file_name: The name of the zip file to create.
    """
    try:
        with zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, folder_path))
    except Exception as e:
        print(f'An error occurred: {str(e)}')


class Sender:
    def __init__(self, credentials=None):
        self.credentials = credentials

    def connect_to_server(self, host, port):
        try:
            s = socket.socket()
            s.connect((host, port))
            return s
        except Exception as e:
            print(f"Error connecting to {host}:{port}: {str(e)}")
            return None

    def zip_and_send_package(self, package_name, host, port):
        folder_to_zip = os.path.join('packages', package_name)
        zip_file_name = package_name + '.zip'
        zip_folder(folder_to_zip, zip_file_name)
        s = self.connect_to_server(host, port)
        
        if s:
            if self.send_file(zip_file_name, s):
                print(f"Package '{package_name}' sent successfully.")
            s.close()
            os.remove(zip_file_name)


    def receive_package_list(self, s):
        try:
            package_list = s.recv(BUFFER_SIZE).decode()
            return package_list
        except Exception as e:
            print(f"Error receiving package list: {str(e)}")
            return ""

    def send_file(self, filename, s):
        try:
            filesize = os.path.getsize(filename)
            s.send(f"{filename}{SEPARATOR}{filesize}".encode())
            progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)

            with open(filename, "rb") as f:
                while True:
                    bytes_read = f.read(BUFFER_SIZE)
                    if not bytes_read:
                        break
                    s.sendall(bytes_read)
                    progress.update(len(bytes_read))
            
            # Close the socket after sending the file
            s.close()
            return True
        except Exception as e:
            print(f"Error sending file {filename}: {str(e)}")
            return False

    def send_command(self, command, host, port):
        s = self.connect_to_server(host, port)
        if s:
            try:
                s.send(f"{command}{SEPARATOR}{self.credentials}".encode())
                response = self.receive_package_list(s)
                print(response)
            except Exception as e:
                print(f"Error sending command: {str(e)}")
            finally:
                # Close the socket
                s.close()


if __name__ == '__main__':
    host = '127.0.0.1'
    host = input("Enter host ip : ")
    port = 5001
    credentials = input("Enter credentials: ")
    sender = Sender(credentials=credentials)
    
    while True:
        package = input("Enter a package to send (or 'exit' to quit): ")
        if package.lower() == 'exit':
            break
        sender.zip_and_send_package(package_name=package, host=host, port=port)
