Goals for part 1:

1.Set up a VM (full-clone VM 9000, and use cloud-init to setup the inital credentials for login and networking. Be sure to provide also an ssh-pubkey).
2.Update the system to the latest packages available. Make also sure you have an editor you're familiar with installed in the VM.
3.Set up a firewall (suggestion: ufw or firewalld) and block all incoming traffic on all ports
4.Setup an ssh server listening on port 2222. Make sure that it is only possible to login with an ssh key and not with a password. Make sure only your user is allowed to log in via ssh. (use openssh and not dropbear). Open port 2222 in the firewall.
5.Setup a wordpress instance behind a reverse proxy, served on https default port with a self-signed certificate (tip: use either Caddy or Nginx. If you use nginx you'll have to generate the certificate yourself). Make sure to open the https port on the firewall.
6.Setup zabbix-agent2, so that it will accept connections from the server from Part 2 (ask whoever you're working with the address for their VM). Make sure to open the zabbix-agent port on the firewall.
Steg 1:
- Downloading ubuntu 20.04 iso file.(Link:https://releases.ubuntu.com/20.04.4/ubuntu-20.04.4-live-server-amd64.iso?_ga=2.131185999.1337877487.1651661538-1813358124.1651661538)
- Recomenation image from ubuntu: (Link:https://cloud-images.ubuntu.com/focal/)
- We should have a ISO image in proxmox,for create the VM on proxmoxyou have to run this cimmand below:
wget https://ftp.lysator.liu.se/ubuntu-releases/20.04.4/ubuntu-20.04.4-live-server-amd64.iso
-For delet a VM on proxmox we have to use this command: 
>> cat /etc/pve/.vmlist  #List of all VM
>> qm destroy VM-id  # delete VM
