#!/bin/bash

# Check if Ncdu is installed
if ! command -v ncdu &>/dev/null; then
	echo "Ncdu is not installed."
	exit 1
fi

# Uninstall Ncdu
sudo apt-get remove ncdu -y

# Display a message indicating the uninstallation is complete
echo "Ncdu uninstallation completed."
