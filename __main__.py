import pulumi
from provider.airbyte_provider import Source, Destination, Connection
from resources import pulumi_execution
from gcp_resources import gcp_resources

gcp_stuff = gcp_resources()
pulumi_execution(gcp_stuff)
