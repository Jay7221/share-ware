from main import send_file, connect_to_server, zip_and_send_package


if __name__ == '__main__':
    host = input("Enter host ip : ")
    if not host:
        host = '127.0.0.1'
    port = 5001

    s = connect_to_server(host=host, port=port)
    try:
        zip_and_send_package(package_name='ncdu', s=s)
    except Exception as e:
        print(f"Execption occred: {str(e)}")
    finally:
        s.close()
