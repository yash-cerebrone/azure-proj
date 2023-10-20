from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import config
import json
import datetime as dt

def add_to_blob(connection_string, container_name, vm_details, vm_name, credentials):
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    blob_name = f"{vm_name} {dt.datetime.now()}.json"

    blob_client = blob_service_client.get_blob_client(container_name, blob_name)
    blob_client.upload_blob(json.dumps(vm_details))
    
def main(vm_details, vm_name, credentials):
    add_to_blob(config.CONNECTION_STRING, config.CONTAINER_NAME, vm_details, vm_name, credentials)