FROM ubuntu:16.04

USER root
RUN apt-get update && apt-get install -y openssh-server
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/g' /etc/ssh/sshd_config
RUN /etc/init.d/ssh restart
RUN apt-get update
RUN apt-get -y install python3.5 python3-pip python3-dev
RUN apt-get -y install ipython ipython-notebook
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install jupyter
RUN pip install qiskit
RUN pip install IBMQuantumExperience
ENTRYPOINT service ssh start && /bin/bash
