from aws_cdk import (
    aws_ecs_patterns as ecs_patterns,
    aws_ecs as ecs,
    aws_ecr_assets as ecr,
    aws_ec2 as ec2,
    aws_servicediscovery as sd,
    core
)


class JenkinsMaster(core.Stack):

    def __init__(self, scope: core.Stack, id: str, cluster, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.cluster = cluster

        # Building a custom image for jenkins master.
        self.container_image = ecr.DockerImageAsset(
            self, "JenkinsMasterDockerImage",
            directory='./docker/'
        )

        # Task definition details to define the Jenkins master container
        self.jenkins_task = ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
            image=ecs.ContainerImage.from_ecr_repository(self.container_image.repository),
            container_port=8080,
            enable_logging=True,
            environment={
                # https://github.com/jenkinsci/docker/blob/master/README.md#passing-jvm-parameters
                'JAVA_OPTS': '-Djenkins.install.runSetupWizard=false'
            },
        )

        ########## EC2 ##########
        # Create the Jenkins master service
        #self.jenkins_master_service = ecs_patterns.ApplicationLoadBalancedEc2Service(
        #    self, "JenkinsMasterService",
        #    cpu=4096,
        #    memory_limit_mib=8192,
        #    cluster=self.cluster,
        #    desired_count=1,
        #    enable_ecs_managed_tags=True,
        #    task_image_options=self.jenkins_task,
        #    cloud_map_options=ecs.CloudMapOptions(name="master"),
        #)

        #self.jenkins_master_service.cluster.add_capacity(
        #    "Ec2",
        #    instance_type=ec2.InstanceType("t3.xlarge"),
        #    key_name="jenkinsonaws"
        #)
        ########## END EC2 ##########

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
