#!/bin/bash

# Check if the script is run as root
if [ "$EUID" -ne 0 ]; then
	echo "Please run this script as root using sudo."
	exit 1
fi

# List all Python-related packages
python_packages=$(dpkg -l | grep '^ii' | grep -E 'python[0-9]\.[0-9]-minimal|python[0-9]\.[0-9]|python3[0-9]\.[0-9]' | awk '{print $2}')

# Remove each Python-related package
for package in $python_packages; do
	apt-get --purge remove -y $package
done

# Autoremove any remaining dependencies
apt-get autoremove -y

# Clean up
apt-get clean

echo "Python and related packages have been removed."
