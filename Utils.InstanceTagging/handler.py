import subprocess
import boto3
import os

ecs_client = boto3.client("ecs")
elb_client = boto3.client("elbv2")
ec2_client = boto3.client("ec2")
client = boto3.resource('ec2')
cloudformation_client = boto3.client("cloudformation")


def handler(event, context):
    aws_tag_key = os.environ.get('aws_tag_key')
    aws_tag_value = os.environ.get('aws_tag_value')

    tag_elb_resources(aws_tag_key, aws_tag_value)
    tag_ec2_instances(aws_tag_key, aws_tag_value)


def tag_elb_resources(aws_tag_key, aws_tag_value):
    untagged_elb_resources = get_untagged_elb_resources(aws_tag_key, aws_tag_value)
    if not untagged_elb_resources:
        print(f"No elb resources was found to be without tag key: {aws_tag_key}")
        return

    print(f"Tagging the following ELB resources with the following tag: {aws_tag_key}:{aws_tag_value}")
    print(untagged_elb_resources)
    for untagged_resource in untagged_elb_resources:
        elb_client.add_tags(ResourceArns=[untagged_resource], Tags=[{"Key": aws_tag_key, "Value": aws_tag_value}])


def tag_ec2_instances(aws_tag_key, aws_tag_value):
    untagged_vpcs = get_untagged_vpcs(aws_tag_key, aws_tag_value)
    untagged_subnets = get_untagged_subnets(aws_tag_key, aws_tag_value)
    untagged_security_groups = get_untagged_security_groups(aws_tag_key, aws_tag_value)
    untagged_ec2_resources = untagged_vpcs + untagged_subnets + untagged_security_groups

    if not untagged_ec2_resources:
        print(f"No EC2 resources was found to be without tag key: {aws_tag_key}")
        return

    print(f"Tagging the following ECS resources with the following tag: {aws_tag_key}:{aws_tag_value}")
    print(untagged_ec2_resources)
    ec2_client.create_tags(Resources=untagged_ec2_resources, Tags=[{"Key": aws_tag_key, "Value": aws_tag_value}])


def get_untagged_vpcs(aws_tag_key, aws_tag_value):
    untagged_vpcs = []
    vpcs = ec2_client.describe_vpcs()
    for vpc in vpcs["Vpcs"]:
        if "Tags" not in vpc.keys() or not tag_exist_on_resource(vpc["Tags"], aws_tag_key, aws_tag_value):
            untagged_vpcs.append(vpc["VpcId"])
    return untagged_vpcs


def get_untagged_subnets(aws_tag_key, aws_tag_value):
    untagged_subnets = []
    subnets = ec2_client.describe_subnets()
    for subnet in subnets["Subnets"]:
        if "Tags" not in subnet.keys() or not tag_exist_on_resource(subnet["Tags"], aws_tag_key, aws_tag_value):
            untagged_subnets.append(subnet["SubnetId"])
    return untagged_subnets


def get_untagged_security_groups(aws_tag_key, aws_tag_value):
    untagged_security_groups = []
    security_groups = ec2_client.describe_security_groups()
    for security_group in security_groups["SecurityGroups"]:
        if "Tags" not in security_group.keys() or not tag_exist_on_resource(security_group["Tags"], aws_tag_key, aws_tag_value):
            untagged_security_groups.append(security_group["GroupId"])
    return untagged_security_groups


def get_untagged_elb_resources(aws_tag_key, aws_tag_value):
    untagged_resources = []
    loadbalancers = elb_client.describe_load_balancers()
    target_groups = elb_client.describe_target_groups()

    loadbalancer_arns = [loadbalancer["LoadBalancerArn"] for loadbalancer in loadbalancers["LoadBalancers"]]
    target_groups_arns = [target_group["TargetGroupArn"] for target_group in target_groups["TargetGroups"]]

    complete_arn_list = target_groups_arns + loadbalancer_arns
    resource_tags = elb_client.describe_tags(ResourceArns=complete_arn_list)

    for resource in resource_tags["TagDescriptions"]:
        tag_exist = tag_exist_on_resource(resource["Tags"], aws_tag_key, aws_tag_value)
        if not tag_exist:
            untagged_resources.append(resource["ResourceArn"])
    return untagged_resources



def tag_exist_on_resource(tags, aws_tag_key, aws_tag_value):
    for tag in tags:
        if aws_tag_key.lower() in [value.lower() for value in tag.values()]:  # Converting to lower case to make it case insensitive
            return True
    return False