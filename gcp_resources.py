import pulumi
import pulumi_gcp as gcp
from dotenv import load_dotenv

load_dotenv()


def gcp_resources():
    config = pulumi.Config("pulumi_airbyte")
    bqowner = gcp.serviceaccount.Account("bqowner2", account_id="bqowner2", project=config.require_secret('gcpProject'))

    dataset = gcp.bigquery.Dataset("dataset",
                                   project=config.require_secret('gcpProject'),
                                   dataset_id="airbyte_pulumi_2",
                                   friendly_name="test",
                                   description="This is a test description",
                                   location="europe-west2",
                                   default_table_expiration_ms=3600000,
                                   labels={
                                       "env": "default",
                                   },
                                   accesses=[
                                       gcp.bigquery.DatasetAccessArgs(
                                           role="OWNER",
                                           user_by_email=bqowner.email,
                                       ),
                                   ])

    pulumi.export("jira_dataset", dataset.id)
    pulumi.export("jira_servce_account", bqowner.id)
    return {"dataset": dataset}
