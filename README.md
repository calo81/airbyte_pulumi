## Simple Pulumi Airbyte Example

This project shows a very simple implementation of a Pulumi provider for Airbyte

### We'll cover

- Creating a simple Airbyte provider
  - The provider will allow create, update and delete resources
  - We'll create Generic Sources and more Specific ones as example
- Create resources that depend on other resources from out-of-the-box providers
  - In particular, we'll use the GCP provider to create BigQuery Datasets and Service Accounts
- Create a Stack (dev). We could use one stack per environment for example (dev, stg and prd)
- Use GCS as the State store
- Configure secrets that are encrypted in the state store
- Create a full Airbyte example
  - Jira Source
  - Bigquery Destination
- Run with
  - `pulumi up`
  - From the IDE (including a DEBUG session)


### Main commands:

```bash
brew install pulumi/tap/pulumi
pulumi new pulumi_airbyte
pulumi stack init dev2
pulumi login --local
pulumi config set pulumi_airbyte:gcpProject "playground-testing-364317"
pulumi config set --secret jiraApiToken = "ATATT3xFfGF0DwXxxxx"
pulumi config set --secret serviceAccountJson '{  "type": "service_account",  "proj..."

pulumi preview
pulumi up

pulumi login gs://pulumi-state-carlo

```