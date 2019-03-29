# Quantum Computing in the Cloud
A Cloud based solution where Quantum computers are allocated as a container running on VCL (Virtual Computing Lab) instance to the user on demand. This container system utilizes Jupyter notebook. IBM Quantum simulators are used to execute Quantum algorithms.

Prerequisites
An account must be created and an API token generated from the IBM Q Experience and pasted in Qconfig.py file.
Host Machine on which application is tested: Ubuntu 16.04..5 LTS (Xenial Xerus)

Installation - Following commands are executed in order to set up the infrastructure
sudo apt-get install docker.io  
sudo apt-get -y install python3.5 python3-pip python3-dev  
python3 -m pip install --upgrade pip  
pip install --user flask  
pip install --user pyyaml  
sudo apt-get install python-yaml  
sudo groupadd docker  
sudo usermod -aG docker $USER  
sudo iptables -I INPUT -p tcp --dport 1000 -j ACCEPT  
Code Files description
main.py - Application entry file
Dockerfile - Creates Jupyter container with necessary dependencies
Qconfig.py - contains the IBM Quantum API token
metadata.yaml - stores details of the container to be created next
script.py - contains method to create new container
user_data.json - contains user details
/templates - Folder contains the html template files
Execution
In your terminal, run the following command to run the application:

sudo python3 main.py
