# PROXMOX
Proxmox Virtual Environment is a type-1 hypervisor. or can think of it as “VirtualBox as a distro”. and must be installed as an operating system directly on the computer. we are trying to install it on a viral machine.
Create Proxmox virtual machine in VirtualBox
Open VirtualBox and click on Machine and New or press CTRL+N to create a new virtual machine.

- Name: proxmox

- typ: Linux

- version: Debian 64bit

- memorysize : 8 GB

- Hard disk : Choose Create a virtual hard disk now and click on Create.

- Hard disk file type: We choose vmdk because it is easier to move to server if needed.

- Storage on physical hard disk:Choose Dynamically allocated and click on Create.

- we changed the size of hard file type to 40 GB and click on create.

- Enable nested VT-X /AMD in the GUI and we changed the processors to 4 CPU.

- We go to network option and choose the Bidged Adapter

- On the storage uder controller: IDE we click on small image of disk under attributes and choose the disk file then click on OK .

- Now you can start your VM

- After start the VM the first page of proxmax will be opend.

- you have to choose install proxmox VE.

- Choose your location and language and click on next

- Enter the password and the email address(pass:Breakingbad!)

- You already have the IP address defined because it was assigned via DHCP, the hostname is : proxmox-ve.local

- You will get the summary of the configuration

- You must uncheck this option because we would need to remove the installation media before we go ahead and reboot

- after this you have to click on install.

- after installation In the Devices-> Optical Drives -> Uncheck the Proxmox iso image that was already checked.

- Click on Force Unmount on the prompt. After that, you may click on Reboot on the installation wizard.

- To access the web GUI, you may type the URL that you see on the Proxmox CLI and you have to write http://IP adressen:port

- You will get a security warning which is expected. You may ignore that and click on Advanced and then choose accept the risk and continue.

- Now you get a proxmox VE login and there you have to write user name : root and pass : Breakingbad!. That is very important to change the realm to Linux PAM standard authentication.
