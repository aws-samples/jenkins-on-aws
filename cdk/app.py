#!/usr/bin/env python3
from aws_cdk import (
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_elasticloadbalancingv2 as elbv2,
    core,
)

class JenkinsECS(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, *kwargs)

        # Create a cluster
        vpc = ec2.Vpc(
            self, "JenkinsVpc",
            max_azs=3
        )

        cluster = ecs.Cluster(
            self, 'EcsCluster',
            vpc=vpc
        )
        cluster.add_capacity("DefaultAutoScalingGroup",
                            instance_type=ec2.InstanceType.of(
                                ec2.InstanceClass.STANDARD5,
                                ec2.InstanceSize.LARGE),
                            desired_capacity=1,
                            max_capacity=2    
                            )

        # Create Task Definition
        task_definition = ecs.Ec2TaskDefinition(
            self, "TaskDef")
        container = task_definition.add_container(
            "web",
            image=ecs.ContainerImage.from_registry("jenkins/jenkins"),
            logging=ecs.LogDrivers.aws_logs(stream_prefix="Jenkins"),
            memory_reservation_mib=6144
        )
        port_mapping = ecs.PortMapping(
            container_port=8080,
            host_port=8080,
            protocol=ecs.Protocol.TCP
        )
        container.add_port_mappings(port_mapping)

        # Create Service
        service = ecs.Ec2Service(
            self, "Service",
            cluster=cluster,
            task_definition=task_definition
        )

        # Create ALB
        lb = elbv2.ApplicationLoadBalancer(
            self, "LB",
            vpc=vpc,
            internet_facing=True
        )
        listener = lb.add_listener(
            "PublicListener",
            port=80,
            open=True
        )

        health_check = elbv2.HealthCheck(
            interval=core.Duration.seconds(60),
            path="/health",
            timeout=core.Duration.seconds(5)
        )

        # Attach ALB to ECS Service
        listener.add_targets(
            "ECS",
            port=8080,
            targets=[service],
            health_check=health_check,
        )

        core.CfnOutput(
            self, "LoadBalancerDNS",
            value=lb.load_balancer_dns_name
        )

app = core.App()
JenkinsECS(app, "JenkinsProd")
app.synth()
