#!/usr/bin/env python3

from aws_cdk import core
from os import getenv

from cdk.network import Network
from cdk.ecs import ECSCluster
from cdk.jenkins_master import JenkinsMaster

stack_name = 'JenkinsOnAWS'
account = getenv('CDK_DEFAULT_ACCOUNT')
region = getenv('CDK_DEFAULT_REGION')

service_discovery_namespace = 'jenkins'

app = core.App()
network = Network(app, stack_name + 'Network')
ecs_cluster = ECSCluster(app, stack_name + 'ECS', vpc=network.vpc, service_discovery_namespace=service_discovery_namespace)
jenkins_master_service = JenkinsMaster(app, stack_name + 'JenkinsMaster', cluster=ecs_cluster.cluster)

app.synth()
