import pulumi
from resources import pulumi_execution
from gcp_resources import gcp_resources
from pulumi.automation import create_or_select_stack
from pulumi.automation import LocalWorkspace
from pulumi.automation import LocalWorkspaceOptions
from pulumi.automation import ProjectBackend
from pulumi.automation import ProjectSettings


def program():
    gcp_stuff = gcp_resources()
    pulumi_execution(gcp_stuff)


if __name__ == "__main__":
    project_name = "pulumi_airbyte"
    stack_name = "dev2"
    stack = pulumi.automation.create_or_select_stack(stack_name=stack_name, project_name=project_name,
                                                     program=program,
                                                     work_dir=".",
                                                     opts=pulumi.automation.LocalWorkspaceOptions(
                                                         project_settings=ProjectSettings(
                                                             name=project_name,
                                                             runtime='python',
                                                             backend=ProjectBackend("gs://pulumi-state-carlo")
                                                         ),
                                                         work_dir="."))
    up_res = stack.up(on_output=print)
