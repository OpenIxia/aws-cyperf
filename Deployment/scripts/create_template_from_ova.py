#!/usr/bin/env python
import os
import json


def CreateTemplate(vcenterName, vsphere_user, vsphere_password, vsphere_datastore, vsphere_src_template, vsphere_src_ova, vsphere_resource_pool_host, vsphere_vswitch_mgmt, vsphere_vswitch_test):

    with open('options_template.json') as opt:
        data = json.load(opt)
    
    network_flag = 0
    for item in data['NetworkMapping']:
        if (item['Name']=="Management Network") :
            network_flag = 1
        if (network_flag==1) :
            item['Network'] = item['Network'].replace('MGMT-VSWITCH', vsphere_vswitch_mgmt)
        
        if (item['Name']=="Test Network") :
            network_flag = 2
        if (network_flag==2) :
            item['Network'] = item['Network'].replace('TEST-VSWITCH', vsphere_vswitch_test)
            
    with open('options.json', 'w') as op:
        json.dump(data, op, indent=4)

    govc_line1="GOVC_URL="+str(vsphere_user)+":"+ "\""+str(vsphere_password)+"\""+"@"+str(vcenter_name)+"/sdk GOVC_INSECURE=1 govc import.ova -options options.json -host="+str(vsphere_resource_pool_host)+ " -ds="+str(vsphere_datastore)+ " -name="+str(vsphere_src_template)+ " "+str(vsphere_src_ova)
    govc_line2="GOVC_URL="+str(vsphere_user)+":"+ "\""+str(vsphere_password)+"\""+"@"+str(vcenter_name)+"/sdk GOVC_INSECURE=1 govc vm.markastemplate "+str(vsphere_src_template)
    print("Copying ova to vCenter {0}".format(vcenter_name))
    print(govc_line1)
    stream1 = os.popen(govc_line1)
    output1= stream1.read()
    output1
    print("Creating template {0} in the vCenter {1}".format(vsphere_src_template,vcenter_name))
    print(govc_line2)
    stream2 = os.popen(govc_line2)
    output2= stream2.read()
    output2

if os.path.exists("../config/user_configurations.json"):
    with open("../config/user_configurations.json") as json_obj:
        input_data=json.load(json_obj)
        # print(input_data)
        for raw_key,raw_value in input_data.items():
            # print(raw_key,raw_value,"\n")
            #line=str(raw_key)+" = "+ "\""+str(raw_value)+"\""+"\n"
            # print(raw_key)
            if (raw_key=="vsphere_vcenter") :
                vcenter_name=raw_value
            elif (raw_key=='vsphere_user'):
               vsphere_user=raw_value
            elif (raw_key=='vsphere_password'):
                vsphere_password=raw_value
            elif (raw_key=='vsphere_datastore'):
                vsphere_datastore=raw_value
            elif (raw_key=='vsphere_src_template'):
                vsphere_src_template=raw_value
            elif (raw_key=='vsphere_resource_pool_host'):
                vsphere_resource_pool_host=raw_value
            elif (raw_key=='vsphere_src_ova'):
                vsphere_src_ova=raw_value
            elif (raw_key=='vsphere_vswitch_mgmt'):
                vsphere_vswitch_mgmt=raw_value
            elif (raw_key=='vsphere_vswitch_test'):
                vsphere_vswitch_test=raw_value


        CreateTemplate(vcenter_name, vsphere_user, vsphere_password, vsphere_datastore, vsphere_src_template, vsphere_src_ova, vsphere_resource_pool_host, vsphere_vswitch_mgmt, vsphere_vswitch_test)
else:
    print("../config/user_configurations.json file not found ")



#Copy ova in the current directory
#1. GOVC_URL=<vCenter username>:"<vCenter password>"@<vCenter IP>/sdk GOVC_INSECURE=1 govc import.ova -host=<resource pool host> -ds=<datastore name> -name=cyperfAgent_<build no>_template <cyperf ova>
#2. GOVC_URL=<vCenter username>:"<vCenter password>"@<vCenter IP>/sdk GOVC_INSECURE=1 govc vm.markastemplate cyperfAgent_<build no>_template
