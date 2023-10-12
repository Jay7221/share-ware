#!/bin/bash

# Remove Node.js and npm
sudo apt-get purge -y nodejs npm

# Remove the NodeSource repository
sudo rm -rf /etc/apt/sources.list.d/nodesource.list

# Update package lists
sudo apt-get update

# Manually remove any residual directories
sudo rm -rf /usr/lib/node_modules

# Manually remove any residual configuration files
sudo rm -rf /etc/npmrc /usr/local/bin/npm /usr/local/share/man/man1/node* /usr/local/lib/dtrace/node.d /usr/local/include/node /usr/local/share/doc/node
