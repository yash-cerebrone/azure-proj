from azure.identity import DefaultAzureCredential, UsernamePasswordCredential, ClientSecretCredential, ManagedIdentityCredential
import config

def get_default_credential():
    return DefaultAzureCredential()

def get_client_credential():
    return ClientSecretCredential(config.TENANT_ID, config.CLIENT_ID, config.SECRET_VALUE)

def get_managed_id_credential():
    return ManagedIdentityCredential()

if __name__=='__main__':
    print(get_managed_id_credential)