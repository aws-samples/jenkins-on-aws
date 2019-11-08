from aws_cdk import (
    aws_ecs_patterns as ecs_patterns,
    aws_ecs as ecs,
    aws_ecr_assets as ecr,
    aws_ec2 as ec2,
    aws_servicediscovery as sd,
    core
)


class JenkinsWorker(core.Stack):

    def __init__(self, scope: core.Stack, id: str, cluster, vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.cluster = cluster
        self.vpc = vpc

        # Building a custom image for jenkins master.
        self.container_image = ecr.DockerImageAsset(
            self, "JenkinsWorkerDockerImage",
            directory='./docker-worker/'
        )

        # Task definition details to define the Jenkins worker container
        self.jenkins_worker = ecs.FargateTaskDefinition(
            self, "ECSJenkinsWorker",
            cpu=1024,
            memory_limit_mib=2048,
        )

        self.jenkins_worker.add_container(

        )

        ################## FARGATE ######################
        # Create the Jenkins master service
        self.jenkins_master_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self, "JenkinsMasterService",
            cpu=4096,
            memory_limit_mib=8192,
            cluster=self.cluster,
            desired_count=1,
            enable_ecs_managed_tags=True,
            task_image_options=self.jenkins_task,
            cloud_map_options=ecs.CloudMapOptions(name="master", dns_record_type=sd.DnsRecordType('A'))
        )
        ################## END FARGATE ######################

        # Opening port 5000 for master <--> worker communications
        self.jenkins_master_service.task_definition.default_container.add_port_mappings(
            ecs.PortMapping(container_port=5000, host_port=5000)
        )
