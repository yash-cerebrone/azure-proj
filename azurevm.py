from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.compute import ComputeManagementClient
import config
import auth

def get_metrics_of_vm(vm_name, resource_group, credential, subscription_id):
    compute_client = ComputeManagementClient(credential, subscription_id)
    keys_to_skip=['os_profile']
    try:
        vm_details = compute_client.virtual_machines.get(resource_group_name=resource_group, vm_name=vm_name)
        for n, i in vm_details.as_dict().items():
            if n in keys_to_skip: continue
            print(f"{n}: {i}")
            print()

        return vm_details.as_dict()
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def list_all_vms(credential, subscription_id):
    compute_client = ComputeManagementClient(credential, subscription_id)
    vm_list = compute_client.virtual_machines.list_all()
    print("Azure Virtual Machines:")
    for vm in vm_list:
        print(f"VM Name: {vm.name}")

def main(credential):
    print("This is for Azure virtual Machines")
    print("Enter vm name or all for all vms")
    choice=input("Enter your choice: ")

    if choice.lower()=='all':
        list_all_vms(credential, config.SUBSCRIPTION_ID)
    else:
        return get_metrics_of_vm(choice, config.RESOURCE_GROUP, credential, config.SUBSCRIPTION_ID), choice

if __name__=='__main__':
    main(auth.get_client_credential())