from main import receive_file, setup_server, receive_package
if __name__ == '__main__':
    s = setup_server()
    client_socket, address = s.accept()
    print(f"Received connection {address}")
    receive_file(client_socket=client_socket)
    # receive_package(client_socket=client_socket)
    print('Done receiving')
    client_socket.close()
    s.close()