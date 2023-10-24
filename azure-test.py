import json
import datetime as dt
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.identity import DefaultAzureCredential, UsernamePasswordCredential, ClientSecretCredential, ManagedIdentityCredential

class config:
    NAME="pythonApp-wasif"
    CONTAINER_NAME='sample-container'
    SUBSCRIPTION_ID = '94ba27d6-505e-44e4-ae1d-0a39c5296f06'
    CONNECTION_STRING='DefaultEndpointsProtocol=https;AccountName=azuretrialsa;AccountKey=GbztdRF8zA+CCRX24Fj+Z4c4+ZAjnQpjThkqMut8JU4YVgpM8jSi1hu5/cHhyoxUORx+HfvVKPGi+ASt3Zc+iA==;EndpointSuffix=core.windows.net'
    RESOURCE_GROUP='myResourceGroup'

def get_default_credential():
    return DefaultAzureCredential()

def get_client_credential():
    return ClientSecretCredential(config.TENANT_ID, config.CLIENT_ID, config.SECRET_VALUE)

def get_managed_id_credential():
    return ManagedIdentityCredential()

def get_metrics_of_vm(vm_name, resource_group, credential, subscription_id):
    compute_client = ComputeManagementClient(credential, subscription_id)
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
    main(get_default_credential())