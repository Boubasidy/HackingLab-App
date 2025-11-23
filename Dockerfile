FROM ubuntu:22.04

# Installer SSH et outils légers
RUN apt-get update && \
    apt-get install -y \
        openssh-server \
        sudo \
        nano \
        curl \
        wget \
        iputils-ping \
        net-tools \
        htop \
        iproute2 && \
    mkdir /var/run/sshd && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Créer l'utilisateur Bouba
RUN useradd -m -s /bin/bash Bouba && \
    echo "Bouba:BoubaSidy" | chpasswd && \
    adduser Bouba sudo

EXPOSE 22

CMD ["/usr/sbin/sshd","-D"]

