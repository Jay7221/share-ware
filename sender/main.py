# Import module
import os
import tkinter as tk
import threading
from tkinter import Tk, StringVar, OptionMenu, Button, Label, Entry, messagebox, ttk
from sender_utils import install_package, delete_package

import time
import ipaddress


def generate_ips(network_mask):
    try:
        network = ipaddress.IPv4Network(network_mask, strict=True)
        all_ips = list(map(str, network.hosts()))

        return all_ips
    except ValueError as e:
        return str(e)


NETWORK_MASK = '10.40.12.0/24'
HOSTS = generate_ips(NETWORK_MASK)
PORTS = [5001]


def on_address_change(*args):
    global NETWORK_MASK
    NETWORK_MASK = address_var.get()


def install():
    package_name = selected_package.get()
    label.config(text=f"Installing {package_name}")
    try:
        for host in generate_ips(NETWORK_MASK):
            for port in PORTS:
                try:
                    install_package(package_name=package_name,
                                    host=host, port=port)
                except AttributeError as e:
                    print(f"Exception occured: {e}")
    except Exception as e:
        print(f"Exception occured: {e}")
    messagebox.showinfo("Package Installed",
                        "Package has been installed on avaliable PCs")




def delete():
    package_name = selected_package.get()
    label.config(text=f"Deleting {package_name}")
    try:
        for host in generate_ips(NETWORK_MASK):
            for port in PORTS:
                try:
                    delete_package(package_name=package_name, host=host, port=port)
                except Exception as e:
                    print(f"Exception occured: {e}")
    except Exception as e:
        print(f"Exception occured: {e}")
    messagebox.showinfo("Package Deleteion",
                        "Package has been deleted on avaliable PCs")

install_thread = threading.Thread(target=install)
delete_thread = threading.Thread(target=delete)
def install_button():
    install_thread.start()

def delete_button():
    delete_button.start()

def stop_download():
    pass

# Create object
root = Tk()

# Adjust size
root.geometry("200x200")
root.title("Share-Ware")

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
button = Button(root, text="Stop", command=stop_download).pack()

# Create Label
label = Label(root, text="Network Address : ")
label.pack()

address_var = StringVar()
address_var.set(NETWORK_MASK)
address_entry = Entry(root, textvariable=address_var)
address_entry.pack()

address_var.trace("w", on_address_change)

# Execute tkinter
root.mainloop()
