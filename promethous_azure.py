from azure.mgmt.monitor import MonitorManagementClient
from azure.identity import DefaultAzureCredential, ClientSecretCredential
from prometheus_client import start_http_server, Gauge
import time, pprint

class config:
    NAME="pythonApp-wasif"
    CONTAINER_NAME='sample-container'
    SUBSCRIPTION_ID = '94ba27d6-505e-44e4-ae1d-0a39c5296f06'
    CONNECTION_STRING='DefaultEndpointsProtocol=https;AccountName=yashtrailsa;AccountKey=GHFVkFYajz1fbyEW1uZWZgs9L1uFTpnFMKqeiyQ7Q9ymop130yEB2VcgJV2ltDmdA5yN9FD/GSUH+AStQ/GCJg==;EndpointSuffix=core.windows.net'
    RESOURCE_GROUP='cerebrone-interns'

def get_default_credential():
    return DefaultAzureCredential()

def get_metric_data(resource_id, credential, subscription_id):
    monitor_client = MonitorManagementClient(
        credential=credential,
        subscription_id=subscription_id
    )

    metrics_data = monitor_client.metrics.list(
        resource_uri=resource_id,
        # timespan="2022-10-01T00:00:00Z/2022-10-30T00:00:00Z",
        interval=None,
        metricnames="Percentage CPU",
        aggregation="Total",
        result_type="Data"
    )

    return metrics_data.as_dict()

def collect_metrics(azure_metric, resource_id, credential, subscription_id):
    # Collect metrics from Azure (use the previous snippet)
    # ...
    metric_value = get_metric_data(resource_id, credential, subscription_id)['value'][0]['timeseries'][0]['data'] # Assume this is the metric value you've collected from Azure
    for i in metric_value:
        if 'total' in i.keys():
            print(i, end=' ')
            azure_metric.set(i['total'])
    print()


if __name__ == '__main__':
    # Start up the server to expose the metrics.
    azure_metric = Gauge('azure_percentage_cpu', 'Percentage CPU used by the Azure resource')
    start_http_server(8000)
    resource_id="/subscriptions/94ba27d6-505e-44e4-ae1d-0a39c5296f06/resourcegroups/cerebrone-interns/providers/Microsoft.Compute/virtualMachines/yash-vm-trial"
    while True:
        print('Collecting metrics...')
        collect_metrics(azure_metric, resource_id, get_default_credential(), config.SUBSCRIPTION_ID)
        print('Sleeping...')
        time.sleep(60)
    # pprint.pprint(get_metric_data(resource_id, get_default_credential(), config.SUBSCRIPTION_ID)['value'][0]['timeseries'][0]['data'])