import auth
import json
import datetime as dt
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.compute import ComputeManagementClient

class config:
    NAME="pythonApp-wasif"
    CLIENT_ID = "ffa67c36-1028-4db8-97b6-6b77a6b066ba"
    CLIENT_SECRET = '18e2ac7c-d020-4934-95f3-7f4ed6183445' #"11df3ad7-d55c-4f86-abf8-943335af25e1"
    TENANT_ID = "3836575b-e523-4f7b-8ce2-deea7cb389b3"
    SECRET_VALUE="2Q48Q~~HLa2pPX5HqRBzQ4CKioqddqKtRzC68dac"
    SUBSCRIPTION_ID = '94ba27d6-505e-44e4-ae1d-0a39c5296f06'
    RESOURCE_GROUP = 'cerebrone-interns'
    MI_CLIENT_ID = 'f5fa6336-4655-4bdf-97f5-11dec1605857'
    CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=yashsatrial;AccountKey=u3fqqPGRptWmu4YQ44cy4JZG0O5L0dgJtsUfaKYdk/Aulsl0GR2RrGVTW9uRvCYjF6IhnyLXv5L9+AStTmVjBw==;EndpointSuffix=core.windows.net"
    CONTAINER_NAME='sample-container'

def get_metrics_of_vm(vm_name, resource_group, credential, subscription_id):
    compute_client = ComputeManagementClient(credential, subscription_id)
    keys_to_skip=['os_profile']
    try:
        vm_details = compute_client.virtual_machines.get(resource_group_name=resource_group, vm_name=vm_name)
        return vm_details.as_dict()
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def list_all_vms(credential, subscription_id):
    compute_client = ComputeManagementClient(credential, subscription_id)
    vm_list = compute_client.virtual_machines.list_all()
    return vm_list

def add_to_blob(connection_string, container_name, vm_details, vm_name):
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    blob_name = f"{vm_name} {dt.datetime.now()}.json"

    blob_client = blob_service_client.get_blob_client(container_name, blob_name)
    blob_client.upload_blob(json.dumps(vm_details))
    print("Upload successful!")

def main(credential):
    for i in list_all_vms(credential, config.SUBSCRIPTION_ID):
        vm_details=get_metrics_of_vm(i.name, config.RESOURCE_GROUP, credential, config.SUBSCRIPTION_ID)
        add_to_blob(config.CONNECTION_STRING, config.CONTAINER_NAME, vm_details, i.name)

if __name__=='__main__':
    main(auth.get_default_credential())