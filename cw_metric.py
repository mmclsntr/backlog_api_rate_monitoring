import boto3


def put_metric(namespace, metric_name, dimensions, metric_value):
    dimensions_list = []
    for name, value in dimensions.items():
        dimensions_list.append({"Name": name, "Value": value})
    cloudwatch = boto3.client('cloudwatch')
    cloudwatch.put_metric_data(
        MetricData=[
            {
                'MetricName': metric_name,
                'Dimensions': dimensions_list,
                'Unit': 'Count',
                'Value': metric_value,
                'StorageResolution': 1
            },
        ],
        Namespace=namespace
    )
