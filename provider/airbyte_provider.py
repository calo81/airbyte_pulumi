import pulumi
from pulumi.dynamic import Resource, ResourceProvider, CreateResult, UpdateResult
import requests

AIRBYTE_API_URL = "http://localhost:8006/v1"  # Update with your Airbyte API URL


class SourceProvider(ResourceProvider):
    def create(self, inputs):
        headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }
        response = requests.post(f"{AIRBYTE_API_URL}/sources", json=inputs, headers=headers)
        response_data = response.json()
        source_id = response_data["sourceId"]
        outputs = {**inputs, "id": source_id}
        return CreateResult(id_=source_id, outs=outputs)

    def update(self, id, olds, news):
        update_data = {**news, "sourceId": id}
        requests.patch(f"{AIRBYTE_API_URL}/sources/{id}", json=update_data)
        return UpdateResult(outs=news)

    def delete(self, id, props):
        requests.delete(f"{AIRBYTE_API_URL}/sources/{id}", json={"sourceId": id})


class DestinationProvider(ResourceProvider):
    def create(self, inputs):
        response = requests.post(f"{AIRBYTE_API_URL}/destinations", json=inputs)
        response_data = response.json()
        destination_id = response_data["destinationId"]
        outputs = {**inputs, "id": destination_id}
        return CreateResult(id_=destination_id, outs=outputs)

    def update(self, id, olds, news):
        update_data = {**news, "destinationId": id}
        requests.patch(f"{AIRBYTE_API_URL}/destinations/{id}", json=update_data)
        return UpdateResult(outs=news)

    def delete(self, id, props):
        requests.delete(f"{AIRBYTE_API_URL}/destinations/{id}", json={"destinationId": id})


class ConnectionProvider(ResourceProvider):
    def create(self, inputs):
        response = requests.post(f"{AIRBYTE_API_URL}/connections", json=inputs)
        response_data = response.json()
        connection_id = response_data["connectionId"]
        outputs = {**inputs, "id": connection_id}
        return CreateResult(id_=connection_id, outs=outputs)

    def update(self, id, olds, news):
        print("UPDATING WITH: ")
        response = requests.patch(f"{AIRBYTE_API_URL}/connections/{id}", json=news)
        print("RESPONSE: " + response.text + " " + str(response.status_code))
        return UpdateResult(outs=news)

    def delete(self, id, props):
        requests.delete(f"{AIRBYTE_API_URL}/connections/{id}", json={"connectionId": id})


class Source(Resource):
    def __init__(self, the_name, opts=None, **props):
        super().__init__(SourceProvider(), the_name, props, opts)


class Destination(Resource):
    def __init__(self, the_name, opts=None, **props):
        super().__init__(DestinationProvider(), the_name, props, opts)


class Connection(Resource):
    def __init__(self, the_name, opts=None, **props):
        super().__init__(ConnectionProvider(), the_name, props, opts)


class JiraSource(Source):
    def __init__(self, the_name, *, workspace, name, api_token, domain, email, opts=None):
        configuration = {"workspaceId": workspace, "name": name,
                         "configuration": {"sourceType": "jira",
                                           "api_token": api_token,
                                           "domain": domain,
                                           "email": email}}
        super().__init__(the_name, opts, **configuration)
