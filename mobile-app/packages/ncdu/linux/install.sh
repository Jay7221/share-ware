#!/bin/bash

# Define the path to the Debian package
deb_package="./ncdu_1.15.1-1_amd64.deb"

# Check if the package file exists
if [ ! -f "$deb_package" ]; then
	echo "Error: Debian package not found."
	exit 1
fi

# Install Ncdu from the Debian package
sudo dpkg -i "$deb_package"

# Install any missing dependencies (if needed)
sudo apt-get install -f -y

# Display a message indicating the installation is complete
echo "Ncdu installation completed."
