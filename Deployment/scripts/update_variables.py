#!/usr/bin/env python
import os
import json

def GetVMName(vmPrefix, vmIndex):
    return "{\n\t"+"\thostname ="+" \""+vmPrefix+"_"+str(vmIndex)+"\"\n \t}"

def UpdateVMNames(tfVarFile, vmCount, vmPrefix):
    line="vm_name = [\n"
    file_obj.write(line)
    count=1
    for i in range(1, vmCount):
        line="\t{0},\n".format(GetVMName(vmPrefix, count))
        file_obj.write(line)
        count=count+1
    line="\t{0}\n]".format(GetVMName(vmPrefix, count))
    file_obj.write(line)

if os.path.exists("../config/user_configurations.json"):
    file_obj=open("../terraform/terraform.tfvars",'w')
    #print("json file exists")
    with open("../config/user_configurations.json") as json_obj:
        input_data=json.load(json_obj)
        # print(input_data)
        for raw_key,raw_value in input_data.items():
            # print(raw_key,raw_value,"\n")
            line=str(raw_key)+" = "+ "\""+str(raw_value)+"\""+"\n"
            # print(raw_key)
            if (raw_key!="vm_count" and raw_key!="vm_prefix") :
               if (raw_key=="vsphere_src_ova" or raw_key=="VarNatsBrokerUrl" or raw_key=="VarManagementInterface" or raw_key=="VarTestInterface" or raw_key=="VarAppsecInstaller" ) :
                  print("skip updating terraform variables")   
               else:
                  file_obj.write(line)
            elif (raw_key=='vm_count'):
                number_of_vms=int(raw_value)
            elif (raw_key=='vm_prefix'):
                vm_prefix=raw_value
                
            # file_obj.close()
        UpdateVMNames(file_obj, number_of_vms, vm_prefix)
        file_obj.close()
else:
    print("../config/user_configurations.json file not found ")

if os.path.exists("../config/user_configurations.json"):
    file_obj=open("../ansible/variables.yml",'w')
    #print("json file exists")
    with open("../config/user_configurations.json") as json_obj:
        input_data=json.load(json_obj)
        # print(input_data)
        file_obj.write("---\n")
        for raw_key,raw_value in input_data.items():
            # print(raw_key,raw_value,"\n")
            line=str(raw_key)+": "+ "\""+str(raw_value)+"\""+"\n"
            # print(raw_key)
            if (raw_key=='VarNatsBrokerUrl'):
                file_obj.write(line)
                #VarNatsBrokerUrl:raw_value
            elif (raw_key=='VarManagementInterface'):
                file_obj.write(line)
                #VarManagementInterface:raw_value
            elif (raw_key=='VarTestInterface'):
                file_obj.write(line)
                #VarTestInterface:raw_value
            elif (raw_key=='VarAppsecInstaller'):
                file_obj.write(line)
                #VarAppsecInstaller:raw_value

        # file_obj.close()
        file_obj.close()
else:
    print("../config/user_configurations.json file not found ")

