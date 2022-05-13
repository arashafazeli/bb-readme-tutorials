## Ansible Install
- Ansible documentaion ==> https://docs.ansible.com/ansible/latest/index.html
- Dooes not work on Windows, if you run windows you need to start a virtual machine.
- create folder to where to install ansible.
- If you want create a virtual environment to install on.
- Install ansible - python3 -m pip install ansible.
- ansible --version to check it installed and see your version.
- ansible -help to get what flags to use.


## Prometheus VM / Ansible
- Create a VM for to run prometheus on, or you can use the Vagrantfile in the repository
    To start the VM use command: vagrant up prometheus
- Now enter the prometheus VM, vagrant ssh prometheus.
- Check status - systemctl status ssh.service
- Check so ssh listening on the right port using: sudo ss -tulpn
- Create yaml-files, one for inventory, which ip to monitor, see the repository for example, or just use that.
    Use git pull, clone or fetch if you want the repo.

     Ansible as an inventory is a list of servers and devices we want to automate. 
     All == target all machines
     Hosts = list of all hosts
     children = sub groups
        webservers
        db servers = database

     So if we run commando and target webservers we will only run the hosts we specofy from webservers and same as if we target
     db servers.

- There are two default groups all and ungrouped. Target ungrouped and only the gost under "all" will be targeted.
- Add a ssh-keygen to your prometheus VM.
- To make all a little bit more easy to follow you can change hostname on prometheus VM to prometheus ==> 
    sudo hostnamectl set-hostname prometheus
- To use the inventory file with ansible:
    - cli ==> ansible -i inventory.yml all -m ping (here "all" is the target) (all means all hosts, -m module)
    - If you running on a authentication error still try adding the user, like this:
        ansible -u vagrant -i inventory.yml all -m ping (-u = user "vagrant" is the user in the prometheus VM)
- To check uptime on prometheus with ansible:
    ansible -u vagrant -i inventory.yml all -a "uptime".
- Create a second yaml-file there is one in the repo as well you can use. It is called prometheus.yml.

- name: Prometheus Playbook ==> name of playbook
  hosts: monitoring ==> what host to target from inventory file
  tasks: ==> what to do
    - name: Ping targets ==> name of task
      ping: ==> what module to use.
    - name: Get hostname ==> name of task
      shell: "hostname" ==> what module to use.
    - name: Get uptime
      shell: "uptime"
- ansible-playbook -u vagrant -i inventory.yml prometheus.yml
    ansible commando | username | what inventory file | what playbook to run.
- Another command for a playbook:
    ---
    - name: Prometheus Playbook
    hosts: monitoring
    tasks:
        - name: Print all available facts
        ansible.builtin.debug:
            var: ansible_facts

- Will print all facts about the VM-

- To set up a playbook more like a playbook in real life, see the docs:
  https://docs.ansible.com/ansible/latest/user_guide/playbooks_intro.html 
  
  See also the prometheus.yml-file in the repo.

  Here is a short example:
    ---
- name: Prometheus Playbook
  hosts: monitoring
  become: true ==> become means you will run this command as root (sudo), can be run on playbook lvl or tasks-lvl
  tasks:
    - name: Update system
      ansible.builtin.apt:
        update_cache: true
        name: '*'
        state: latest

- If you run in to an issue with sudo and it tells you that password is missing, add -K flag to ansible command.
  "ansible-playbook -u vagrant -i inventory.yml prometheus.yml -K" 

  -Next is to create a new user:
        - name: Create user
      ansible.builtin.user:
        name: lura
        comment: Created by Ansible
        uid: 2000
        password: 
        state: present (create new user) absent (removes user)

    To add a password we dont want to add our actuall password, but a hashed version of our password.
    To do this, run "sudo apt install whois" ==> mkpasswd --method=sha-512 ==> enter a password (password123) and copy the hashed passwrd that shows.


## Install prometheus
- Official docs: https://prometheus.io/docs/prometheus/latest/installation/

- Prometheus tool to monitor traffic on your website. Checks incoming requests. Collects data. 
- Most common to use prometheus to collect data and Grafan to visualize data.

- To add to your ansible (prometheus) yml-file:

  - Set hostname:
    - name: Set hostname
      ansible.builtin.hostname:
      name: prometheus-server
      use: systemd

      - name: Download prometheus executable
      ansible.builtin.get_url:
        url: https://github.com/prometheus/prometheus/releases/download/v2.35.0/prometheus-2.35.0.linux-amd64.tar.gz
        dest: /home/vagrant/

    - name: Extract prometheus
      ansible.builtin.unarchive:
        src: prometheus-2.35.0.linux-amd64.tar.gz ==> local source
        dest: . ==> destination source/folder
        remote_src: true ==> remote source == true.

- Run your yml-file again with ansible: ansible-playbook -u vagrant -i inventory.yml prometheus.yml
  If all is ok you can enter your prometheus VM and check that you got an extracted file called prometheus something.
- Go to your prometheus VM.
- Time to configure the prometheus.yml file (not same file as before).
- change directory (cd) to the prometheus folder.
  in VM cli type: sudo ./prometheus --config.file=prometheus.yml

- If you turn the program off and go to "less prometheus.yml" we see that server is running on localhost:9090 and collecting matrix from it self. This will need to be changed.
- type this command: sudo ./prometheus --config.file=prometheus.yml --web.listen-address="0.0.0.0:9090" And now we listen to all addresses
- Now we need to open port 9090, lets do that through ansible (the local prometheus.yml-file)
  Add this:

    - name: Open prometheus port in firewall
      community.general.ufw:
        rule: allow
        port: 9090
        proto: tcp
        direction: in

  run the ansible command: ansible-playbook -u vagrant -i inventory.yml prometheus.yml
  Go back to prometheus VM, check status: sudo ufw status verbose

- Now run this commando again on your VM: sudo ./prometheus --config.file=prometheus.yml --web.listen-address="0.0.0.0:9090"
- Go to your browser type: http://192.168.56.12:9090/metrics ip of your VM:port/metrics
- Now change /metrics to /graph to enter a web GUI.
  
  To check incoming requests you can enter in the search field: promhttp_metric_handler_requests_total
  And to check only incoming requests with 200 ok and rate: rate(promhttp_metric_handler_requests_total{code="200"}[1m])

## Install Grafana
- Open source to build graphs for monitoring and visualize data.
- prometheus docs for grafana: https://prometheus.io/docs/visualization/grafana/ 
- Grafanas docs: https://grafana.com/grafana/download

  - Go to Grafanas docs.
  choose open source
  Linux (or what os you have)
  Now open the prometheus.yml (locally, the ansible file) -file and add the Grafana download and extract command:

    - name: Download Grafana binary
      ansible.builtin.get_url:
        url: https://dl.grafana.com/oss/release/grafana-8.5.2.linux-amd64.tar.gz
        dest: /home/vagrant/

    - name: Extract Grafana
      ansible.builtin.unarchive:
        src: grafana-8.5.2.linux-amd64.tar.gz
        dest: /home/vagrant/
        remote_src: true
    
  Run the ansible-playbook command: ansible-playbook -u vagrant -i inventory.yml prometheus.yml
- Go in to Grafana folder.
- We will do som config.
- Go defaults.ini in conf folder, run: less conf/defaults.ini
  Check server rows that it looks good, default should work.

- Go to the local ansible-file (prometheus.yml) add grafans port to firewall:

    - name: Open Grafana port in firewall
      community.general.ufw:
        rule: allow
        port: 3000
        proto: tcp
        direction: in

  Run: ansible-playbook -u vagrant -i inventory.yml prometheus.yml

- Now we can run: sudo ./bin/grafana-server
- Go to VM ip port 3000: http://192.168.56.12:3000
- grafana should start, username and password is admin as defualt. 
  You will be asked to creeate your own password afterwards.

## Grafana GUI
- Go to settings ==> data sources ==> prometheus
- Add prometheus.
  => under HTTP, add URL.
  => URL = Since Grafana and prometheus runs on the same VM we can just type: http://localhost:9090 (prometheus runs on port 9090).

- Now cliv save & test
- Now go to dashboard settings ==> data source ==> prometheus ==> dashboard.
  There are three add ons we can import, add all three.

- Go to dashboard ==> browse
  Here you will find all three imports and can click on them to see different graphs.

- Go to prometheus2.0, on the top roght corner there is a "add panel" click on that.
  Now a squere will appear. Click on "Add new panel", here we can type as in prometheus earlier, for example: 
    ==> rate(promhttp_metric_handler_requests_total{code="200"}[1m])
  
## Grafana, nice prometheus settings

- Make sure you use prometheus on Grafana: Settings ==> data sources ==> add data source ==> prometheus and add config as above.
- Go to dashboard and import dashboard.
- Add panel, set title to the right "title". Add Metrics in Metrix browser.
- Click on top right corner, "time series" and choose different type of graphs you like.

- If you like to see som actions on the dashboard we can send some fake requests with this command:
  for I in $(seq 10000); do curl http://192.168.56.12:9090/metrics >/dev/null 2>&1; done

  for loop through a sequence of, in this case 10 000 times, then curl the VM ip and port to send all  10 000 requests.

- On top right corner we can add scope with time range. It is a small "clock"-symbol.

- If you like prometheus to scrape more often, close the prometheus server, go to the config file ==> "sudo nano prometheus.yml"
  On the top there is a line called: "global" ==> "scrape_interval: " it is set default to 15s, you can change to 1 sec to 
  scrape more real time.

## Set up node.js

- Find the node.js file in the https://prometheus.io/download/
- Add this lines to the playbook (prometheus.yml-file):

    - name: Download prometheus node exporter
      ansible.builtin.get_url:
        url: https://github.com/prometheus/node_exporter/releases/download/v1.3.1/node_exporter-1.3.1.linux-amd64.tar.gz
        dest: /home/vagrant/

    - name: Extract node exporter
      ansible.builtin.unarchive:
        src: node_exporter-1.3.1.linux-amd64.tar.gz
        dest: /home/vagrant/
        remote_src: true

  Run the ansible-playbook-command: ansible-playbook -u vagrant -i inventory.yml prometheus.yml

  Now the node.js-file should be on your VM and extracted.

- In your VM cd into the new node-folder.
- Run this command: sudo ./node_exporter
- Open the terminal-window where prometheus is running and stop it for a little while.
- Open the promethes config-file: sudo nano prometheus.yml
  Add a target under "static_configs" ==> "localhost:9100".
  Start the prometheus server again.

- Go back to grafana, add a new panel:
- Now we should be able to find and use node metrics.
- metrics, try to add this: rate(node_network_transmit_bytes_total[1m])
- title "Network transmit"
- Click on apply, then top right corner of dashboard click on save ==> save as ==> add like "custom" to title to make it your own panel. 
- Add a panel again, this time to monitor free memory, add metric: node_memory_MemFree_bytes.
- Click on Transform, we will transform this bytes to megabytes.
- Add transformation, "mode: binary operation", operation: click down the arrow and choose the one existing. add a
  divide sign and type "1024". Add one more of these exact transformations.

To check that the free memory actually is accurate, go to your prometheus VM and type: "watch -n 1 free --mebi"