#!/usr/bin/env python3

from aws_cdk import core
from os import getenv

from jenkins.network import Network
from jenkins.ecs import ECSCluster
from jenkins.jenkins_master import JenkinsMaster
from jenkins.jenkins_worker import JenkinsWorker

stack_name = 'JenkinsOnAWS' # TODO: Source this as an environment variable
account = getenv('CDK_DEFAULT_ACCOUNT')
region = getenv('CDK_DEFAULT_REGION')

service_discovery_namespace = 'jenkins'

app = core.App()
network = Network(app, stack_name + 'Network')
ecs_cluster = ECSCluster(app, stack_name + 'ECS', vpc=network.vpc, service_discovery_namespace=service_discovery_namespace)
jenkins_workers = JenkinsWorker(app, stack_name + "Worker", vpc=network.vpc, cluster=ecs_cluster)
jenkins_master_service = JenkinsMaster(app, stack_name + 'JenkinsMaster', cluster=ecs_cluster, vpc=network, worker=jenkins_workers)

app.synth()
