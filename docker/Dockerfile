# Dockerfile minimal pour secure-ssh
FROM ubuntu:22.04

# Installation de SSH et netcat (pour healthcheck)
RUN apt-get update && \
    apt-get install -y openssh-server netcat && \
    mkdir /var/run/sshd && \
    useradd -m -s /bin/bash user1 && \
    echo 'user1:password' | chpasswd && adduser user1 sudo && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin no/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

# Healthcheck : vérifie que SSH répond
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD nc -z localhost 22 || exit 1

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]
