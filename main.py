import azurevm
import azurebs
import auth
import config

credentials = auth.get_default_credential()

services={1:"Virtual Machine", 2:"Blob Storage"}
for n, i in services.items():
    print(f"{n}:{i}")
service = int(input("Enter the service you want to interact with: "))

if service == 1:
    vm_details, vm_name=azurevm.main(credentials)
    azurebs.main(vm_details, vm_name, credentials)
