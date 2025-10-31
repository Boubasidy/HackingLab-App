# Dockerfile minimal pour secure-ssh
FROM ubuntu:22.04

# Installer OpenSSH
RUN apt-get update && \
    apt-get install -y openssh-server sudo && \
    mkdir /var/run/sshd

# Création utilisateur
RUN useradd -m -s /bin/bash user1 && echo "user1:password" | chpasswd && adduser user1 sudo

EXPOSE 22

CMD ["/usr/sbin/sshd","-D"]

