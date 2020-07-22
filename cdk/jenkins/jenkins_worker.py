from aws_cdk import (
    aws_ecr_assets as ecr,
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_logs as logs,
    core
)

from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

class JenkinsWorker(core.Stack):

    def __init__(self, scope: core.Stack, id: str, vpc, cluster, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.vpc = vpc
        self.cluster = cluster

        # Building a custom image for jenkins leader.
        self.container_image = ecr.DockerImageAsset(
            self, "JenkinsWorkerDockerImage",
            directory='./docker/worker/'
        )

        # Security group to connect workers to leader
        self.worker_security_group = ec2.SecurityGroup(
            self, "WorkerSecurityGroup",
            vpc=self.vpc,
            description="Jenkins Worker access to Jenkins leader",
        )

        # IAM execution role for the workers to pull from ECR and push to CloudWatch logs
        self.worker_execution_role = iam.Role(
            self, "WorkerExecutionRole",
            assumed_by=iam.ServicePrincipal('ecs-tasks.amazonaws.com'),
        )

        self.worker_execution_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name(
            'service-role/AmazonECSTaskExecutionRolePolicy'
            )
        )

        # Task role for worker containers - add to this role for any aws resources that jenkins requires access to
        self.worker_task_role = iam.Role(
            self, "WorkerTaskRole",
            assumed_by=iam.ServicePrincipal('ecs-tasks.amazonaws.com'),
        )

        # Create log group for workers to log
        self.worker_logs_group = logs.LogGroup(
            self, "WorkerLogGroup",
            retention=logs.RetentionDays.ONE_DAY
        )

        # Create log stream for worker log group
        self.worker_log_stream = logs.LogStream(
            self, "WorkerLogStream",
            log_group=self.worker_logs_group
        )

