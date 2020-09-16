#!/usr/bin/env python
import os
import json
import subprocess

# Deploy VMs
stream1 = os.popen('terraform init')
output1= stream1.read()
output1
stream2 = os.popen('terraform plan')
output2= stream2.read()
output2
stream3 = os.popen('terraform apply -auto-approve')
output3= stream3.read()
output3

# Fetch IPs of Deployed VM
debug = 0
inventory=[]

output_json_str = subprocess.check_output(['terraform', 'output', '-json', 'VM_ip'])

json_object = json.loads(output_json_str)

#inventory = list(json_object['value'])
inventory = json_object

for item in inventory:
 print item[0]


