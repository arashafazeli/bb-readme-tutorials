## Proxmox installation
Proxmox Virtual Environment is a type-1 hypervisor. Think of it as “VirtualBox as a distro”. 
It must be installed as an operating system directly on the computer but we are installng it on a viral machine..it is not recomended! (but hey, we are breaking bad)

## Create a Proxmox virtual machine 
- Download proxmox iso file https://www.proxmox.com/en/downloads/item/proxmox-ve-7-2-iso-installer
- Open VirtualBox and click on Machine and New or press CTRL+N to create a new virtual machine. 

      Our settings:

      - Name: proxmox
      - Type: Linux
      - Version: Debian 64bit
      - Memorysize : 8 GB (minimum 1gb)
      - Hard disk : Choose Create a virtual hard disk now and click on Create.
      - Hard disk file type: We choose vmdk because it is easier to move to server if needed.
      - Storage on physical hard disk:Choose Dynamically allocated and click on Create.
      - Change size of hard file type to 40 GB and click on create (minimuim 8gb).
      - Enable nested VT-X /AMD in the GUI and we changed the processors to 4 CPU.
      - Go to network option and choose the Bidged Adapter
      - On the storage uder controller: 
        IDE we click on small image of disk under attributes and choose the downloaded iso disk file then click on OK.
      - Now you can start your VM

After start the VM the first page of proxmax will be opend.

    - Choose install proxmox VE.
    - Choose location and language and click on next
    - Enter password and the email address
    - You already have the IP address defined because it was assigned via DHCP, 
      Dubbelcheck that the IP adress is in the same "IP-spann" as your computers. 
    - Fully qualified domain name (FQDN) is : proxmox-ve.local
    - Check summary of the configuration. 
    - You must uncheck "autoreboot after installation" because we would need to remove the 
      installation media before we go ahead and reboot
    - After this you have to click on install.
    - After installation in the Devices-> Optical Drives -> Uncheck the Proxmox iso image.
    - Click on Force Unmount on the prompt. After that, you may click on Reboot on the installation wizard.

To access the web GUI, the URL that is shown in the Proxmox CLI. Don't forget to write http://

      - You will get a security warning which is expected. Click on Advanced and then choose accept the risk and continue.
      - Now you get a proxmox VE login.
      - Change the realm to Linux PAM standard authentication.
      - Username : root 
      - Pass : ----
