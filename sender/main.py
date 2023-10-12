# Import module
import os
from tkinter import Tk, StringVar, OptionMenu, Button, Label
from sender_utils import install_package, delete_package

import ipaddress


def generate_ips(network_mask):
    try:
        network = ipaddress.IPv4Network(network_mask, strict=False)
        all_ips = list(map(str, network.hosts()))

        return all_ips
    except ValueError as e:
        return str(e)

NETWORK_MASK = '127.1.0.0/24'
HOSTS = generate_ips(NETWORK_MASK)
PORTS = [5001]

# Create object
root = Tk()

# Adjust size
root.geometry("200x200")
root.title("Share-Ware")


def install():
    package_name = selected_package.get()
    label.config(text=f"Installing {package_name}")
    for host in HOSTS:
        for port in PORTS:
            try:
                install_package(package_name=package_name, host=host, port=port)
            except Exception as e:
                print(f"Exception occured: {e}")


def delete():
    package_name = selected_package.get()
    label.config(text=f"Deleting {package_name}")
    for host in HOSTS:
        for port in PORTS:
            try:
                delete_package(package_name=package_name, host=host, port=port)
            except Exception as e:
                print(f"Exception occured: {e}")


# Dropdown menu options
packages = os.listdir('packages/')

# datatype of menu text

selected_package = StringVar()

# initial menu text
selected_package.set("nodejs")

# Create Dropdown menu
drop = OptionMenu(root, selected_package, *packages)
drop.pack()

# Create button, it will change label text
button = Button(root, text="Install", command=install).pack()
button = Button(root, text="Delete", command=delete).pack()

# Create Label
label = Label(root, text=" ")
label.pack()

# Execute tkinter
root.mainloop()
