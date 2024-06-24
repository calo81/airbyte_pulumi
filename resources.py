import pulumi
from provider.airbyte_provider import Source, Destination, Connection, JiraSource
from dotenv import load_dotenv
from gcp_resources import gcp_resources

load_dotenv()


def pulumi_execution(gcp_resources):
    config = pulumi.Config("pulumi_airbyte")
    dataset = gcp_resources["dataset"]
    workspace_id = config.require('airbyte_workspace'),
    # Jira Source configuration
    jira_source_config = {"workspaceId": workspace_id, "name": "Personal Jira 8",
                          "configuration": {"sourceType": "jira",
                                            "api_token": config.require_secret('jiraApiToken'),
                                            "domain": config.require_secret('jira_domain'),
                                            "email": config.require_secret('jira_email')}}

    # BigQuery Destination configuration
    bigquery_destination_config = {"workspaceId": workspace_id, "name": "BigQuery Destination 3xxx", "configuration": {
        "destinationType": "bigquery",
        "dataset_location": "europe-west2",
        "project_id": config.require_secret('gcpProject'),
        "dataset_id": dataset.dataset_id,
        "credentials_json": config.require_secret('serviceAccountJson'),
        "loading_method": {
            "method": "Standard"
        }
    }
                                   }

    # Create Jira Source
    jira_source = Source("jiraSource", **jira_source_config)

    jira_source2 = JiraSource("jiraSourceTheSecond",
                              name="Jira Source Alternative 5",
                              workspace=workspace_id,
                              domain=config.require_secret('jira_domain'),
                              email=config.require_secret('jira_email'),
                              api_token=config.require_secret('jiraApiToken'))

    # Create BigQuery Destination
    bigquery_destination = Destination("bigQueryDestination", **bigquery_destination_config)

    # Create Connection linking Jira Source and BigQuery Destination
    connection_config = {
        "name": "The Connection 5",
        "sourceId": jira_source.id,
        "destinationId": bigquery_destination.id,
        "schedule": {"scheduleType": "manual"},
        "namespaceDefinition": "destination",
        "namespaceFormat": None,
        "nonBreakingSchemaUpdatesBehavior": "ignore",
        "configurations": {"streams": [
            {
                "syncMode": "full_refresh_overwrite",
                "name": "issues"
            }
        ]}
    }

    connection = Connection("jiraToBigQueryConnection2", **connection_config)

    connection_config_2 = {
        "name": "The Connection Alternative 9",
        "sourceId": jira_source2.id,
        "destinationId": bigquery_destination.id,
        "schedule": {"scheduleType": "manual"},
        "namespaceDefinition": "destination",
        "namespaceFormat": None,
        "nonBreakingSchemaUpdatesBehavior": "ignore",
        "configurations": {"streams": [
            {
                "syncMode": "full_refresh_overwrite",
                "name": "issues"
            }
        ]}
    }

    connection2 = Connection("jiraToBigQueryConnectionAlternative4", **connection_config_2)

    connection_config_3 = {
        "name": "The Connection Alternative XXX 9",
        "sourceId": jira_source2.id,
        "destinationId": bigquery_destination.id,
        "schedule": {"scheduleType": "manual"},
        "namespaceDefinition": "destination",
        "namespaceFormat": None,
        "nonBreakingSchemaUpdatesBehavior": "ignore",
        "configurations": {"streams": [
            {
                "name": "projects",
                "syncMode": "full_refresh_overwrite",
            },
            {
                "syncMode": "incremental_deduped_history",
                "name": "issues"
            }
        ]}
    }

    connection3 = Connection("jiraToBigQueryConnectionAlternativeXXX4", **connection_config_3)

    pulumi.export("jira_source_id", jira_source.id)
    pulumi.export("bigquery_destination_id", bigquery_destination.id)
    pulumi.export("connection_id", connection.id)
    pulumi.export("connection_id_2", connection2.id)
    pulumi.export("connection_id_3", connection3.id)
    pulumi.export("jira_source2_id", jira_source2.id)
