## Table of Contents

### Directory Tree

    ./Agility2018/
    ├── playbooks
    │   ├── f5_drift.yml
    │   ├── files
    │   │   ├── extra_vars.yml
    │   │   ├── passwords_cleartext.yml
    │   │   ├── passwords.yml
    │   │   └── vip_input.json
    │   ├── inventory
    │   │   └── hosts.yml
    │   ├── library
    │   │   └── firewall_change_audit.py
    │   └── vip_firewall.yml
    └── README.md


### playbooks

#### f5_drift.yml
Demonstration playbook which illustrates using a dynamic inventory in Ansible with the Service Now *lb* table as the source of truth. It opens tickets for BIG-IP devices which are not at the desired version.

#### vip_firewall.yml
Demonstration playbook shown in the You Tube video, the first play retrieves configuration data from the MongoDB, the second play applies ACLs to firewall(s), retrieves the firewall configs, updates the audit database and updates the ServiceNow change ticket for each firewall in the group.

#### library
The Python program, `firewall_change_audit.py` illustrates how the audit database can be queried and a simple report generated to show changes made to the router ACL over time, showing the initiating ticket number, the commands issued to the target device, and the time of day. 

#### inventory
File `hosts.yml` is sample Ansible inventory file which identifies which Cisco CSR routers implement the firewall group specified as input to the work flow. It also demonstrates using the *network_cli* plug-in for connecting to network devices.

#### files
The file `vip_input.json` is an example of the JSON object loaded into the MongoDB. The playbook retrieves this data structure from the MongoDB base on the *hostname*, *database*, *collection* and ObjectID passed to the playbook as extra vars. Rather than pass all the variables needed to complete the configuration change to the playbook, we simply pass a pointer on where to retrieve the configuration artifacts.

The file `extra_vars.yml` is simply a means to pass extra vars into an Ansible playbook.

The `passwords_cleartext.yml` is an example of how to pass encrypted credentials to a playbook. Isolating credentials in a separate file is a means of limiting the scope of who has access to credentials.