CyPerf Agent Deployment Model
======================================
This document specifies step by step instructions for deploying CyPerf Agent at vCenter environment. Before referring this document, user need to deploy CyPerf UI/Controller and CyPerf license server by following CyPerf Deployment guide.  

Prerequisite
==================
1.	A vCenter environment along with ESXi hosts connected to the vCenter.
2.	A ubuntu 18.04 controller system to prepare and execute deployment and configuration scripts.

Dependencies
=================
On Ubuntu 18.04, the following packages are required:
•	unzip
•	wget
•	ansible
•	sshpass
•	curl
•	terraform
•	govc
To make your life easier, we provide the install_prerequisite.sh script, which will install all the dependencies needed on Ubuntu 18.04.

Steps
======
Login to your Ubuntu 18.04 controller system.

1.	Download scripts

	Download CyPerf_Deployment_and_Configuration_In_vCenter.tar.gz
	untar CyPerf_Deployment_and_Configuration_In_vCenter.tar.gz file in the Ubuntu 18.04 controller system

2.	Install Prerequisite 

	Execute bellow shell script to prepare CyPerf Deployment and configuration controller environment.
	# cd scripts
	# sudo  ./install_prerequisite.sh

	Note: step 1 and 2 need to execute only once for an environment.

3.	User configuration

        User need to provide following inputs in “user_configurations.json” placed in “config” directory.
a.	"vsphere_vcenter": "<vCenter IP>",
b.	"vsphere_user": "<vCenter username>",
c.	"vsphere_password": "<vCenter password>",
d.	"vsphere_datacenter": "<data center name>",
e.	"vsphere_cluster": "<cluser name>",
f.	"vsphere_datastore": "<data store name>",
g.	"vsphere_src_template": "<source template name>",
h.	"vsphere_src_ova": “<Full path of ova file>”
i.	"vsphere_vswitch_mgmt": "<vSwitch name>", [vSwitch must pre-exists] [Limitation:  terraform script in its current state cannot manage connectivity.]
j.	"vsphere_vswitch_test": "<vSwitch name>", [vSwitch must pre-exists] [Limitation:  terraform script in its current cannot manage connectivity.]
k.	"vsphere_vm_cpu_count": 2,
l.	"vsphere_vm_memory_mb": 4096,
m.	"vm_count": <number of VM want to deploy>,
n.	"vm_prefix" : "<Prefix name for deployed VM>",
o.	“VarNatsBrokerUrl”: "nats://<CyPerf Controller IP>:30422"
p.	“VarManagementInterface”: "<Management interface>"
q.	“VarTestInterface”: "<Test interface>"
r.	“VarAppsecInstaller”: "<CyPerf binary>" # this is needed only for H/W installation [Not required if ova is used]

4.	 Create Template 

	Create a template from ova using GOVC tool. 
	This step needs only once unless user want to change template.

    	 # python create_template_from_ova.py  

5.  	Update variables

      	Update terraform and ansible variables based on user input provided at step 3.
        #  python update_variables.py [Note:  Qualified only with python 2.7]

6. 	 Deploy VMs

	 Deploy CyPerf Agents from template using terraform tool.

         # cd ../terraform
         #python deploy_vm_from_template.py > ../ansible/hosts 
         [ Assumption: Default DHCP configuration for management interface of ova learns IP before timeout. Static IP case not covered yet]

7.       Configure VMs

	 Configure CyPerf agents with configuration management tool ansible.
	 # cd ../ansible

         a. Associate VMs with a CyPerf Controller-

            #ansible-playbook playbook_configure_appsec_ova_vm.yml -i ./hosts -u appsec --extra-vars 'ansible_ssh_pass=appsec' --extra-vars 'ansible_become_pass=appsec'

         b. Restart port manager service-

            #ansible-playbook playbook_restart_portmanager.yml -i ./hosts -u appsec --extra-vars 'ansible_ssh_pass=appsec' --extra-vars 'ansible_become_pass=appsec'

         c. Reboot CyPerf agents -

            #ansible-playbook playbook_reboot_node.yml -i ./hosts -u appsec --extra-vars 'ansible_ssh_pass=appsec' --extra-vars 'ansible_become_pass=appsec'

8.  	Use cases

	     Case 1:  For re-deployment of another set of agents with same ova template, follow bellow instructions
        	    a. Backup terraform.tfstate with your preference name [ example: terraform.tfstate.bkp1 ]
       		    b. update “config/user_configurations.json”. 
       		   [At least need to update "vm_prefix" : "<Prefix name for deployed VM>"]
       		    c. python deploy_vm_from_template.py  > ../ansible/hosts

	     Case 2:  For re-deployment of another set of agents with different ova template, follow bellow instructions
             	    a. Backup “terraform.tfstate” with your preference name [ example: terraform.tfstate.bkp1 ]
      		    b. update “config/user_configurations.json”. 
                    [At least need to update "vm_prefix" : "<Prefix name for deployed VM>"]
                    c. python create_template_from_ova.py
                    d. python deploy_vm_from_template.py

	    Case 3: To destroy current deployed VMs
     		  a. terraform destroy -auto-approve

            Case 4: To destroy previous deployed VM
       		  a. Copy file “terraform.tfstate.bkp1” to “terraform.tfstate”
                  b. terraform destroy -auto-approve

