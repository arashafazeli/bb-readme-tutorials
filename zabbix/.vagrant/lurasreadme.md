## Vagrantfile
- You will need a vagranfile, write one yourself or feel free to use the one in this folder.
    It is a Vagrantfile for VM for Zabbix and a extra klient called api.

## Vagrant
- vagrant init
- have a vagrantfile ready
- vagrant up
- vagrant status (checka att VMs är up and running)
- vagrant ssh zabbix


## Zabbix
- Follow this official documentation / tutorial
- First commando not sudo
- the rest sudo
- https://www.zabbix.com/download?zabbix=6.0&os_distribution=ubuntu&os_version=20.04_focal&db=mysql 
- After first 4 commandos install a mysql-server, "sudo apt install mysql-server"
- sudo systemctl status mysql.service (see if server is running and active. Starts on boot)
- sudo mysql_secure_installation
- If password in mysql_secure.... dont work. Close and sudo into mysql, "sudo mysql".
- Run this command: "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root';" will change root password to
    "root".
- continue on above link tutorial, where "sudo mysql -u root -p" stands.

- Continue with command sudoedit /etc/zabbix/zabbix_server.conf
- scroll to DBuser=zabbix
- uncommment dbpassorwd and add the password, in my case pass is "password".
- continue on link tutorial
- frontend is now up, go to browser and type "192.168.56.10/zabbix/"

## Zabbix frontend
- Click and check all is ok then click next.
- conf db conn, choose correct db type, host is localhost
    port is 0 (0 = use default port), db name is zabbix user is zabbix
    password = password
- settings, add name, default time zone => Europe/Stockholm (also set timezone in vagrant@Ubuntu VM "sudo timedatectl set-timezone Europe/Stockholm), sudo timedatectl to check 
- Installs the frontend and creates this file: conf/zabbix.conf.php", can be good to make a back up.
- If Zabbix server is running = Value = no, check in CLI using this command, "systemctl status zabbix-server.service".
    See that active is == "active (running).

## Login
- Admin is default username
- zabbix is default password

## Zabbix usage
- Monitoring, see dashboard, users, latest data, graphs etc.
- Configuration, conf our user

## Trigger a trigger...
- Trigger uptime trigger.
- Uptime checks every 30 sec.
- If we turn off by force our VM, log out first (logout) Then "vagrant halt -f zabbix".
- "vagrant status" and we will se it has been powered off.
- "vagrant up zabbix" to start the VM again.
- "vagrant ssh zabbix" check (type in CLI) "uptime" will be 0 minutes approx.
- Check for trigger alert on zabbix frontend.


## Add a host
- vagrant status (make sure VM is running)
- vagrant ssh api
- Follow the tutorial again on the link above. (step a)
- Do the first 3 steps to beginn with.
- We do not need to install mysql, server or apache on this VM.
- We need to install zabbix-agent2 ==> "sudo apt install zabbix-agent2".
- check status, "sudo systemctl status zabbix-agent2.service"
- check logs ==> "sudo less /var/log/zabbix/zabbix_agent2.log".
- edit the conf file ==> "sudoedit /etc/zabbix/zabbix_agent2.conf"
    Go to "Option: ListenIP, uncomment ListenIP and set to 192.168.56.11.
    Go to "passive checks related" under "Option Server" add server to talk to (zabbix VM) to "server" == 192.168.56.10
    Remoce localhost.
- Go to "Active checks related, Option: ServerActive, ServerActive=192.168.56.10
- Go to Option: Hostname, uncomment Hostname and add a name, for example = api-srv. Remove hostname=zabbix server.
- Close and save.
- check hostname, "sudo hostnamectl" if the hostname is not the same as in conf-file, change it.
- Change hostname, "sudo hostnamectl set-hostname api-srv".
- logout and login from VM.
- Now the conf has been changed we want to do a reboot so all the agents will read the new conf-file.
- "sudo systemctl restart zabbix-agent2.service"

## Add the new host
- Go to zabbix frontend ==> Configuration ==> Hosts ==> create host.
- hostname same as VM so in this case "api-srv".
- Templates == "Linux by Zabbix agent". Will add items and triggers automatic.
- Groups == "Virtual MAchines" (since this is two VMs)
- Interfaces = Agents, add IP of api-srv == 192.168.56.11, standard port.
- keep enabled on.
- add.
- reboot api-server
- Check status, "systemctl status zabbix-agent2.service"
- If api-srv dont start automatic, try ==> "sudo systemctl enable --now zabbix-agent2.service".

## Add a web scenario, drag down and monitor a http-service
- go to conf, hosts, web.
- Add web scenario
- add a name
- Add a update interval
- Add agent, here we use Zabbix.
- Can be tagged to check scenarios at one time as long as they have same tag.
- go to steps, add a web scenario.
- step of web scenario:
    name
    add url to be fetched
    Can be added queries and redirects etc.
    Retrieve body = Headers
    Timeout = 15s (If it takes more than 15s to fetch url it will be set an alarm.)
    required status code = 200 (OK), if  another status code will be sent it will trigger an alarm.
- To see how scenario goes, click "monitoring, hosts, web".
- In CLI (in API VM) type "sudo python3 -m http.server 80" And we will see when our scenario do the checks and it will be
    be a 200 ok.
- How to create a trigger for our web scenario
    conf, hosts, triggers, create trigger.
- add:
    name: 
    Choose Severity
    Expression = add, our case we will see if status code is 200 or not, so choose "Failed step of scenario "api-srv-scenario".
        Function should be most recent
        Result: = 1
    check allow manual close (does so we can close a trigger and not just acknowledge)
    check enabled
    add.
- To resolve problem start http.server again in CLI "sudo python3 -m http.server 80".

## Get Alarms on email
- Start a docker container (mailhog) from local CLI.
- type following, "docker run -d --rm -p 192.168.56.1:1025:1025 -p 127.0.0.1:8025:8025 mailhog/mailhog:latest"
- if denied run "sudo chmod 666 /var/run/docker.sock"
- Go to localhost:8025
- go to Zabbix frontend
- Admin, Media types, Email or Email(HTML)
    SMTP Server = 192.168.56.1
    port = 1025
    Update.
    far right corner you can test send.
- Add media to user
    Admin, Users, Media, add.
        Media:
        Type: Same as set when setting up media type, my case Email(HTML)
        send to: admin@zabbix.com (doesn't matter since it is Mailhog docker container)
        Turn off "use of severity: Not Classified, info and warning" To get less spam.
- Go to conf, Actions, Trigger Actions, add.
    check enabled, then update

