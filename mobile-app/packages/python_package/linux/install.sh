#!/bin/bash

# Update your system's package list
sudo apt update

# Install essential packages for building software
sudo apt install -y software-properties-common

# Add the repository for Python 3.9
sudo add-apt-repository ppa:deadsnakes/ppa

# Update the package list again
sudo apt update

# Install Python 3.9
sudo apt install -y python3.9
